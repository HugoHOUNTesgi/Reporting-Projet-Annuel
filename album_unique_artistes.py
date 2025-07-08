#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyse de l'hypothèse : Les playlists contiennent plus d'albums uniques que d'artistes 
(forte dispersion album/artiste)

Auteur: Hugo HOUNTONDJI
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings

# Configuration pour l'affichage
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def charger_donnees():
    """Charge les données nettoyées"""
    try:
        df = pd.read_csv('alcrowd/alcrowd_cleaned.csv')
        print(f"Données chargées : {len(df)} lignes et {len(df.columns)} colonnes")
        return df
    except Exception as e:
        print(f"Erreur lors du chargement des données : {e}")
        return None

def analyser_playlists_uniques(df):
    """Analyse les statistiques par playlist unique"""
    # Grouper par playlist pour obtenir les statistiques uniques
    playlists_stats = df.groupby(['name', 'pid']).agg({
        'num_albums': 'first',
        'num_artists': 'first',
        'num_tracks': 'first',
        'artist_name': 'nunique',  # Nombre d'artistes uniques réels
        'album_name': 'nunique',   # Nombre d'albums uniques réels
        'track_name': 'nunique'    # Nombre de tracks uniques réels
    }).reset_index()
    
    # Renommer les colonnes pour plus de clarté
    playlists_stats.rename(columns={
        'artist_name': 'artistes_uniques_reels',
        'album_name': 'albums_uniques_reels',
        'track_name': 'tracks_uniques_reels'
    }, inplace=True)
    
    # Calculer le ratio albums/artistes
    playlists_stats['ratio_albums_artistes'] = (
        playlists_stats['albums_uniques_reels'] / 
        playlists_stats['artistes_uniques_reels']
    )
    
    # Calculer la différence albums - artistes
    playlists_stats['diff_albums_artistes'] = (
        playlists_stats['albums_uniques_reels'] - 
        playlists_stats['artistes_uniques_reels']
    )
    
    return playlists_stats

def analyser_hypothese(playlists_stats):
    """Analyse statistique de l'hypothèse"""
    print("\n" + "="*80)
    print("ANALYSE DE L'HYPOTHÈSE : DISPERSION ALBUM/ARTISTE")
    print("="*80)
    
    # Statistiques descriptives
    print("\n1. STATISTIQUES DESCRIPTIVES")
    print("-"*50)
    print(f"Nombre total de playlists analysées : {len(playlists_stats)}")
    
    print(f"\nAlbums uniques par playlist :")
    print(f"  - Moyenne : {playlists_stats['albums_uniques_reels'].mean():.2f}")
    print(f"  - Médiane : {playlists_stats['albums_uniques_reels'].median():.2f}")
    print(f"  - Écart-type : {playlists_stats['albums_uniques_reels'].std():.2f}")
    
    print(f"\nArtistes uniques par playlist :")
    print(f"  - Moyenne : {playlists_stats['artistes_uniques_reels'].mean():.2f}")
    print(f"  - Médiane : {playlists_stats['artistes_uniques_reels'].median():.2f}")
    print(f"  - Écart-type : {playlists_stats['artistes_uniques_reels'].std():.2f}")
    
    # Test de l'hypothèse principale
    print("\n2. TEST DE L'HYPOTHÈSE PRINCIPALE")
    print("-"*50)
    
    # Pourcentage de playlists avec plus d'albums que d'artistes
    plus_albums = (playlists_stats['albums_uniques_reels'] > 
                   playlists_stats['artistes_uniques_reels']).sum()
    pct_plus_albums = (plus_albums / len(playlists_stats)) * 100
    
    print(f"Playlists avec plus d'albums que d'artistes : {plus_albums}/{len(playlists_stats)} ({pct_plus_albums:.1f}%)")
    
    # Test statistique (test de Wilcoxon pour échantillons appariés)
    statistic, p_value = stats.wilcoxon(
        playlists_stats['albums_uniques_reels'], 
        playlists_stats['artistes_uniques_reels']
    )
    
    print(f"\nTest de Wilcoxon (échantillons appariés) :")
    print(f"  - Statistique : {statistic}")
    print(f"  - p-value : {p_value:.2e}")
    print(f"  - Significatif (α=0.05) : {'Oui' if p_value < 0.05 else 'Non'}")
    
    # Analyse du ratio
    print("\n3. ANALYSE DU RATIO ALBUMS/ARTISTES")
    print("-"*50)
    ratio_moyen = playlists_stats['ratio_albums_artistes'].mean()
    ratio_median = playlists_stats['ratio_albums_artistes'].median()
    
    print(f"Ratio moyen albums/artistes : {ratio_moyen:.3f}")
    print(f"Ratio médian albums/artistes : {ratio_median:.3f}")
    
    # Playlists avec ratio > 1 (plus d'albums que d'artistes)
    ratio_sup_1 = (playlists_stats['ratio_albums_artistes'] > 1).sum()
    pct_ratio_sup_1 = (ratio_sup_1 / len(playlists_stats)) * 100
    
    print(f"Playlists avec ratio > 1 : {ratio_sup_1}/{len(playlists_stats)} ({pct_ratio_sup_1:.1f}%)")
    
    # Distribution de la différence
    print("\n4. ANALYSE DE LA DIFFÉRENCE (ALBUMS - ARTISTES)")
    print("-"*50)
    diff_positive = (playlists_stats['diff_albums_artistes'] > 0).sum()
    pct_diff_positive = (diff_positive / len(playlists_stats)) * 100
    
    print(f"Playlists avec différence positive : {diff_positive}/{len(playlists_stats)} ({pct_diff_positive:.1f}%)")
    print(f"Différence moyenne : {playlists_stats['diff_albums_artistes'].mean():.2f}")
    print(f"Différence médiane : {playlists_stats['diff_albums_artistes'].median():.2f}")
    
    return {
        'pct_plus_albums': pct_plus_albums,
        'p_value': p_value,
        'ratio_moyen': ratio_moyen,
        'ratio_median': ratio_median,
        'pct_ratio_sup_1': pct_ratio_sup_1
    }

def creer_visualisations(playlists_stats, resultats):
    """Crée les visualisations pour l'analyse"""
    
    # Configuration de la figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Analyse de la Dispersion Album/Artiste dans les Playlists', 
                 fontsize=16, fontweight='bold')
    
    # 1. Distribution des albums et artistes uniques
    axes[0, 0].hist(playlists_stats['albums_uniques_reels'], bins=30, alpha=0.7, 
                   label='Albums uniques', color='skyblue')
    axes[0, 0].hist(playlists_stats['artistes_uniques_reels'], bins=30, alpha=0.7, 
                   label='Artistes uniques', color='lightcoral')
    axes[0, 0].set_xlabel('Nombre')
    axes[0, 0].set_ylabel('Fréquence')
    axes[0, 0].set_title('Distribution Albums vs Artistes Uniques')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Scatter plot Albums vs Artistes
    axes[0, 1].scatter(playlists_stats['artistes_uniques_reels'], 
                      playlists_stats['albums_uniques_reels'], 
                      alpha=0.6, s=30)
    # Ligne y=x pour référence
    max_val = max(playlists_stats['artistes_uniques_reels'].max(), 
                  playlists_stats['albums_uniques_reels'].max())
    axes[0, 1].plot([0, max_val], [0, max_val], 'r--', alpha=0.8, linewidth=2, 
                   label='Ligne d\'égalité (y=x)')
    axes[0, 1].set_xlabel('Artistes uniques')
    axes[0, 1].set_ylabel('Albums uniques')
    axes[0, 1].set_title('Relation Albums vs Artistes')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Distribution du ratio Albums/Artistes
    axes[0, 2].hist(playlists_stats['ratio_albums_artistes'], bins=30, 
                   alpha=0.7, color='green', edgecolor='black')
    axes[0, 2].axvline(x=1, color='red', linestyle='--', linewidth=2, 
                      label='Ratio = 1')
    axes[0, 2].axvline(x=resultats['ratio_moyen'], color='blue', linestyle='-', 
                      linewidth=2, label=f'Moyenne = {resultats["ratio_moyen"]:.2f}')
    axes[0, 2].set_xlabel('Ratio Albums/Artistes')
    axes[0, 2].set_ylabel('Fréquence')
    axes[0, 2].set_title('Distribution du Ratio Albums/Artistes')
    axes[0, 2].legend()
    axes[0, 2].grid(True, alpha=0.3)
    
    # 4. Distribution de la différence
    axes[1, 0].hist(playlists_stats['diff_albums_artistes'], bins=30, 
                   alpha=0.7, color='purple', edgecolor='black')
    axes[1, 0].axvline(x=0, color='red', linestyle='--', linewidth=2, 
                      label='Différence = 0')
    axes[1, 0].set_xlabel('Différence (Albums - Artistes)')
    axes[1, 0].set_ylabel('Fréquence')
    axes[1, 0].set_title('Distribution de la Différence Albums - Artistes')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # 5. Box plot comparatif
    data_boxplot = [playlists_stats['artistes_uniques_reels'], 
                    playlists_stats['albums_uniques_reels']]
    axes[1, 1].boxplot(data_boxplot, labels=['Artistes', 'Albums'])
    axes[1, 1].set_ylabel('Nombre d\'éléments uniques')
    axes[1, 1].set_title('Comparaison Box Plot')
    axes[1, 1].grid(True, alpha=0.3)
    
    # 6. Analyse par taille de playlist
    # Créer des catégories de taille
    playlists_stats['categorie_taille'] = pd.cut(
        playlists_stats['num_tracks'], 
        bins=[0, 20, 50, 100, float('inf')], 
        labels=['Petite (≤20)', 'Moyenne (21-50)', 'Grande (51-100)', 'Très grande (>100)']
    )
    
    ratio_par_taille = playlists_stats.groupby('categorie_taille')['ratio_albums_artistes'].mean()
    axes[1, 2].bar(range(len(ratio_par_taille)), ratio_par_taille.values, 
                  color=['lightblue', 'lightgreen', 'lightyellow', 'lightpink'])
    axes[1, 2].set_xticks(range(len(ratio_par_taille)))
    axes[1, 2].set_xticklabels(ratio_par_taille.index, rotation=45, ha='right')
    axes[1, 2].axhline(y=1, color='red', linestyle='--', alpha=0.8)
    axes[1, 2].set_ylabel('Ratio moyen Albums/Artistes')
    axes[1, 2].set_title('Ratio par Taille de Playlist')
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('alcrowd/analyse_dispersion_album_artiste.png', dpi=300, bbox_inches='tight')
    plt.show()

def conclure_hypothese(resultats):
    """Conclusion sur l'hypothèse"""
    print("\n" + "="*80)
    print("CONCLUSION SUR L'HYPOTHÈSE")
    print("="*80)
    
    print("\nHypothèse testée :")
    print("'Les playlists contiennent plus d'albums uniques que d'artistes (forte dispersion album/artiste)'")
    
    print(f"\nRésultats clés :")
    print(f"- {resultats['pct_plus_albums']:.1f}% des playlists ont plus d'albums que d'artistes")
    print(f"- Ratio moyen albums/artistes : {resultats['ratio_moyen']:.3f}")
    print(f"- Test statistique significatif : {'Oui' if resultats['p_value'] < 0.05 else 'Non'} (p = {resultats['p_value']:.2e})")
    
    if resultats['pct_plus_albums'] > 50 and resultats['ratio_moyen'] > 1:
        conclusion = "HYPOTHÈSE CONFIRMÉE"
        explication = ("La majorité des playlists présentent effectivement plus d'albums uniques "
                      "que d'artistes, indiquant une forte dispersion album/artiste.")
    elif resultats['pct_plus_albums'] > 40:
        conclusion = "HYPOTHÈSE PARTIELLEMENT CONFIRMÉE"
        explication = ("Une proportion significative des playlists présente plus d'albums "
                      "que d'artistes, mais ce n'est pas majoritaire.")
    else:
        conclusion = "HYPOTHÈSE RÉFUTÉE"
        explication = ("La majorité des playlists ne présente pas plus d'albums que d'artistes, "
                      "ce qui ne confirme pas l'hypothèse de forte dispersion.")
    
    print(f"\n🎯 CONCLUSION : {conclusion}")
    print(f"\n📊 Explication : {explication}")
    
    # Interprétation métier
    print(f"\n💡 Interprétation métier :")
    if resultats['ratio_moyen'] > 1:
        print("- Les utilisateurs tendent à diversifier les albums plus que les artistes")
        print("- Cela suggère une exploration musicale axée sur la variété des œuvres")
        print("- Les playlists reflètent une curiosité pour différents albums d'un même artiste")
    else:
        print("- Les utilisateurs tendent à explorer plus d'artistes que d'albums")
        print("- Cela suggère une préférence pour la découverte de nouveaux artistes")
        print("- Les playlists reflètent une approche de découverte artistique")

def main():
    """Fonction principale"""
    print("🎵 ANALYSE DE LA DISPERSION ALBUM/ARTISTE DANS LES PLAYLISTS")
    print("="*80)
    
    # Chargement des données
    df = charger_donnees()
    if df is None:
        return
    
    # Analyse des playlists uniques
    print("\n📊 Calcul des statistiques par playlist...")
    playlists_stats = analyser_playlists_uniques(df)
    
    # Analyse de l'hypothèse
    resultats = analyser_hypothese(playlists_stats)
    
    # Création des visualisations
    print("\n📈 Création des visualisations...")
    creer_visualisations(playlists_stats, resultats)
    
    # Conclusion
    conclure_hypothese(resultats)
    
    # Sauvegarde des résultats
    playlists_stats.to_csv('alcrowd/analyse_dispersion_resultats.csv', index=False)
    print(f"\n💾 Résultats sauvegardés dans 'alcrowd/analyse_dispersion_resultats.csv'")

if __name__ == "__main__":
    main()
