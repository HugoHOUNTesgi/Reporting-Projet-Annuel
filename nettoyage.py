# 1_nettoyage.py

# Membres du groupe :
# Hugo HOUNTONDJI
# LO Maty
# HU Angel
# PASINI Georgio

#################################################################################################

# Ce script a pour objectif de :
# Charger les fichiers de données brutes (JSON du MPD).
# Aplatir la structure pour avoir une ligne par piste de playlist.
# Nettoyer les données (gestion des valeurs nulles, des doublons, conversion des types).
# Sauvegarder le jeu de données propre dans un fichier CSV (`alcrowd_cleaned.csv`) qui servira de base pour toutes les analyses futures.

#################################################################################################

# Importation des bibliothèques
import pandas as pd
import os
import glob
import json

print("--- Début du script de nettoyage (1_nettoyage.py) ---")
print("Étape 1: Importation des bibliothèques terminée.")

#################################################################################################

# Chargement et fusion des données
base_dir = os.path.dirname(os.path.abspath(__file__))
alcrowd_path = os.path.join(base_dir, 'alcrowd')
output_dir = alcrowd_path
os.makedirs(output_dir, exist_ok=True)

#################################################################################################

# Chargement des fichiers JSON
json_files = glob.glob(os.path.join(alcrowd_path, 'mpd.slice.*.json'))
all_playlists = []
for file in json_files:
    with open(file, 'r') as f:
        data = json.load(f)
        all_playlists.extend(data['playlists'])

print(f"Chargement de {len(all_playlists)} playlists")

#################################################################################################

# Aplatissement des données (une ligne par piste)
if all_playlists:
    mpd_df = pd.DataFrame(all_playlists)
    mpd_exploded_df = mpd_df.explode('tracks')
    tracks_df = mpd_exploded_df['tracks'].apply(pd.Series)
    mpd_flat_df = pd.concat([mpd_exploded_df.drop(columns=['tracks']), tracks_df], axis=1)
    
    # Renommage des colonnes pour éviter les conflits
    if 'duration_ms' in mpd_flat_df.columns:
        cols = mpd_flat_df.columns.tolist()
        idx_playlist_duration = cols.index('duration_ms')
        cols[idx_playlist_duration] = 'playlist_duration_ms'
        if 'duration_ms' in cols[idx_playlist_duration + 1:]:
            idx_track_duration = cols.index('duration_ms', idx_playlist_duration + 1)
            cols[idx_track_duration] = 'track_duration_ms'
        mpd_flat_df.columns = cols
    
    df = mpd_flat_df.copy()
    print("DataFrame aplati créé avec succès.")
    print("Dimensions initiales :", df.shape)
else:
    raise ValueError("Aucune playlist n'a été chargée. Vérifiez les fichiers JSON.")

#################################################################################################

# Nettoyage des données
print("\nÉtape 3: Début du nettoyage des données.")

#################################################################################################

# Gestion des valeurs manquantes
print(f"Lignes avant suppression des NaN ('track_uri'): {len(df)}")
df.dropna(subset=['track_uri'], inplace=True)
print(f"Lignes après suppression des NaN ('track_uri'): {len(df)}")

if 'description' in df.columns:
    df.drop(columns=['description'], inplace=True)
    print("Colonne 'description' supprimée.")

# Le '0' peut apparaître si une colonne 'tracks' était vide.
if '0' in df.columns and df['0'].isnull().all():
    df.drop(columns=['0'], inplace=True)

#################################################################################################

# Gestion des doublons
print(f"Lignes avant suppression des doublons : {len(df)}")
df.drop_duplicates(inplace=True)
print(f"Lignes après suppression des doublons : {len(df)}")

#################################################################################################

# Conversion des types de données
df['modified_at'] = pd.to_datetime(df['modified_at'], unit='s')
print("Conversion du type de 'modified_at' en datetime.")
print("Dimensions finales après nettoyage :", df.shape)

#################################################################################################

# Sauvegarde des données nettoyées
cleaned_data_path = os.path.join(output_dir, 'alcrowd_cleaned.csv')
df.to_csv(cleaned_data_path, index=False, encoding='utf-8')

print(f"\nNettoyage terminé")
print(f"Les données nettoyées ont été sauvegardées ici : {cleaned_data_path}") 