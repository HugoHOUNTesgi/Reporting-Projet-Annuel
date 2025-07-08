# Membres du groupe :
# Hugo HOUNTONDJI
# LO Maty
# HU Angel
# PASINI Georgio


# Ce script a pour objectif de réaliser une analyse exploratoire sur les données nettoyées.
# Charger le jeu de données nettoyé (`alcrowd_cleaned.csv`).
# Réaliser une analyse univariée pour comprendre la distribution de chaque variable (statistiques descriptives, histogrammes).
# Réaliser une analyse bivariée pour explorer les relations entre les variables (matrice de corrélation).


# Importation des bibliothèques
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


print("Débutons notre analyse exploratoire")
print("Importation des bibliothèques terminée.")

#################################################################################################


# Chargement des données
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, 'alcrowd', 'alcrowd_cleaned.csv')
# Création d'un dossier de sortie dédié pour les graphiques
output_dir = os.path.join(base_dir, 'alcrowd', 'analyse_exploratoire_plots')
os.makedirs(output_dir, exist_ok=True)

if not os.path.exists(data_path):
    raise FileNotFoundError(f"Le fichier de données nettoyées n'a pas été trouvé : {data_path}\n"
                            "Pensez à dans un premier temps, exécuter le script 'de nettoyage des données.")

df = pd.read_csv(data_path)
print(f"Données chargées depuis '{data_path}'.")

#################################################################################################

# Analyse Exploratoire (EDA)
print("\nDébut de l'analyse exploratoire.")

#################################################################################################

# A. Analyse univariée
print("\nStatistiques descriptives des colonnes numériques :")
print(df.describe())

#################################################################################################

# Visualisation des distributions
numeric_cols_to_plot = ['num_followers', 'num_tracks', 'playlist_duration_ms', 'track_duration_ms', 'num_artists', 'num_albums']
plt.figure(figsize=(15, 12))
plt.suptitle('Analyse univariée - Distributions des variables numériques', fontsize=16)
for i, col in enumerate(numeric_cols_to_plot, 1):
    plt.subplot(3, 2, i)
    sns.histplot(df[col], kde=True, bins=50)
    plt.title(f'Distribution de {col}')
    # L'échelle log est utile pour les données très asymétriques
    if df[col].max() > 1000 and df[col].min() >= 0:
        plt.xscale('log')
plt.tight_layout(rect=[0, 0, 1, 0.96])
univariate_plot_path = os.path.join(output_dir, 'univar_1_distributions_numeriques.png')
plt.savefig(univariate_plot_path)
print(f"Graphiques des distributions univariées sauvegardés : {univariate_plot_path}")
plt.close()

#################################################################################################

# Boxplots pour les variables numériques
plt.figure(figsize=(15, 10))
plt.suptitle('Analyse univariée - Boxplots des variables numériques', fontsize=16)
for i, col in enumerate(numeric_cols_to_plot, 1):
    plt.subplot(2, 3, i)
    sns.boxplot(y=df[col])
    plt.title(f'Boxplot de {col}')
    plt.yscale('log')
plt.tight_layout(rect=[0, 0, 1, 0.96])
univariate_box_path = os.path.join(output_dir, 'univar_2_boxplots_numeriques.png')
plt.savefig(univariate_box_path)
print(f"Boxplots sauvegardés : {univariate_box_path}")
plt.close()

#################################################################################################

# Analyse des variables catégorielles (Top 20)
def plot_top_n(data, column, n, title, path):
    plt.figure(figsize=(12, 8))
    top_n = data[column].value_counts().nlargest(n)
    sns.barplot(x=top_n.values, y=top_n.index, palette='viridis')
    plt.title(title)
    plt.xlabel("Nombre d'apparitions")
    plt.ylabel(column.replace('_', ' ').title())
    plt.tight_layout()
    plt.savefig(path)
    print(f"Graphique '{title}' sauvegardé : {path}")
    plt.close()

plot_top_n(df, 'artist_name', 20, 'Top 20 des artistes les plus fréquents', os.path.join(output_dir, 'univar_3_top20_artistes.png'))
plot_top_n(df, 'album_name', 20, 'Top 20 des albums les plus fréquents', os.path.join(output_dir, 'univar_4_top20_albums.png'))


#################################################################################################

# Nuage de mots pour les noms de playlists
playlist_names = ' '.join(df['name'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(playlist_names)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Nuage de mots des noms de playlists')
wordcloud_path = os.path.join(output_dir, 'univar_5_wordcloud_noms_playlist.png')
plt.savefig(wordcloud_path)
print(f"Nuage de mots sauvegardé : {wordcloud_path}")
plt.close()

#################################################################################################

# B. Analyse bivariée
# Matrice de corrélation
numeric_cols = df.select_dtypes(include=np.number).columns
corr_matrix = df[numeric_cols].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=.5)
plt.title('Analyse bivariée - Matrice de corrélation')
bivariate_plot_path = os.path.join(output_dir, 'bivar_1_matrice_correlation.png')
plt.savefig(bivariate_plot_path)
print(f"Matrice de corrélation sauvegardée : {bivariate_plot_path}")
plt.close()

#################################################################################################

# Pairplot pour les variables clés
pairplot_cols = ['num_followers', 'num_tracks', 'track_duration_ms', 'num_artists']
sns.pairplot(df[pairplot_cols].dropna())
plt.suptitle('Analyse bivariée - Pairplot des variables clés', y=1.02)
pairplot_path = os.path.join(output_dir, 'bivar_2_pairplot.png')
plt.savefig(pairplot_path)
print(f"Pairplot sauvegardé : {pairplot_path}")
plt.close()

#################################################################################################

# Scatter plot spécifique
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='num_tracks', y='num_followers', alpha=0.5)
plt.title('Relation entre le nombre de pistes et le nombre de followers')
plt.xlabel('Nombre de pistes')
plt.ylabel('Nombre de followers')
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
scatter_path = os.path.join(output_dir, 'bivar_3_scatter_pistes_followers.png')
plt.savefig(scatter_path)
print(f"Nuage de points sauvegardé : {scatter_path}")
plt.close()

print("\n--- Analyse exploratoire terminée ---")
print(f"Tous les graphiques ont été sauvegardés dans : {output_dir}")

# Fin du script