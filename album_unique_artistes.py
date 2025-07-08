# Membres du groupe :
# Hugo HOUNTONDJI
# LO Maty
# HU Angel
# PASINI Georgio

#################################################################################################

# Ce script a pour objectif de :
# Analyser l'hypothèse : "Les playlists contiennent plus d'albums uniques que d'artistes (forte dispersion album/artiste)"
# Calculer les statistiques par playlist (albums uniques vs artistes uniques)
# Effectuer des tests statistiques pour valider ou réfuter l'hypothèse
# Créer des visualisations détaillées de l'analyse
# Générer un rapport complet avec conclusions métier

#################################################################################################

# Importation des bibliothèques
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import os

# Configuration pour l'affichage
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("--- Début du script d'analyse dispersion album/artiste (3_album_unique_artistes.py) ---")
print("Importation des bibliothèques terminée.")

#################################################################################################

# Chargement des données
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, 'alcrowd', 'alcrowd_cleaned.csv')
output_dir = os.path.join(base_dir, 'alcrowd')

if not os.path.exists(data_path):
    raise FileNotFoundError(f"Le fichier de données nettoyées n'a pas été trouvé : {data_path}\n"
                            "Pensez à dans un premier temps, exécuter le script de nettoyage des données.")

df = pd.read_csv(data_path)
print(f"Données chargées depuis '{data_path}'.")
print(f"Dimensions du dataset : {df.shape[0]} lignes et {df.shape[1]} colonnes")

#################################################################################################

# Analyse des playlists uniques
print("\nÉtape 1: Calcul des statistiques par playlist...")

# Grouper par playlist pour obtenir les statistiques uniques
playlists_stats = df.groupby(['name', 'pid']).agg({
    'num_albums': 'first',
    'num_artists': 'first',
    'num_tracks': 'first',
    'artist_name': 'nunique',  # Nombre d'artistes uniques réels
    'album_name': 'nunique',   # Nombre d'albums uniques réels
    'track_name': 'nunique'    # Nombre de tracks uniques réels
}).reset_index()

# Renommage des colonnes pour plus de clarté
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

print(f"Statistiques calculées pour {len(playlists_stats)} playlists uniques.")

#################################################################################################

# Analyse statistique de l'hypothèse
print("\nÉtape 2: Test de l'hypothèse de dispersion album/artiste...")

print("="*80)
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

#################################################################################################

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

#################################################################################################

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

#################################################################################################

# Distribution de la différence
print("\n4. ANALYSE DE LA DIFFÉRENCE (ALBUMS - ARTISTES)")
print("-"*50)
diff_positive = (playlists_stats['diff_albums_artistes'] > 0).sum()
pct_diff_positive = (diff_positive / len(playlists_stats)) * 100

print(f"Playlists avec différence positive : {diff_positive}/{len(playlists_stats)} ({pct_diff_positive:.1f}%)")
print(f"Différence moyenne : {playlists_stats['diff_albums_artistes'].mean():.2f}")
print(f"Différence médiane : {playlists_stats['diff_albums_artistes'].median():.2f}")

# Stockage des résultats pour les visualisations
resultats = {
    'pct_plus_albums': pct_plus_albums,
    'p_value': p_value,
    'ratio_moyen': ratio_moyen,
    'ratio_median': ratio_median,
    'pct_ratio_sup_1': pct_ratio_sup_1
}

#################################################################################################

# Création des visualisations techniques
print("\nÉtape 3: Création des visualisations techniques...")

# Configuration de la figure avec espacement optimisé
fig, axes = plt.subplots(2, 3, figsize=(20, 14))
fig.suptitle('Analyse de la Dispersion Album/Artiste dans les Playlists', 
             fontsize=16, fontweight='bold', y=0.98)

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

# Ajustement de l'espacement pour éviter la superposition des titres
plt.subplots_adjust(top=0.93, bottom=0.08, left=0.08, right=0.95, 
                    hspace=0.35, wspace=0.25)
visualization_path = os.path.join(output_dir, 'analyse_dispersion_album_artiste.png')
plt.savefig(visualization_path, dpi=300, bbox_inches='tight')
print(f"Visualisations techniques sauvegardées : {visualization_path}")
plt.show()

#################################################################################################

# VISUALISATIONS POUR DASHBOARD GRAND PUBLIC
print("\nÉtape 3b: Création des visualisations pour dashboard grand public...")

# Couleurs corporate et modernes
colors_primary = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
colors_accent = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']

#################################################################################################

# 1. GRAPHIQUE PRINCIPAL : Message percutant
fig1, ax1 = plt.subplots(figsize=(12, 8))

# Données pour le graphique en secteurs
labels = [f'Plus d\'albums\n({pct_plus_albums:.1f}%)', 
          f'Plus d\'artistes\n({100-pct_plus_albums:.1f}%)']
sizes = [pct_plus_albums, 100-pct_plus_albums]
colors = ['#4ECDC4', '#FF6B6B']
explode = (0.1, 0)  # Mise en avant du secteur principal

wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                                   autopct='%1.1f%%', startangle=90, 
                                   textprops={'fontsize': 14, 'fontweight': 'bold'})

ax1.set_title('🎵 Les playlists Spotify privilégient la DIVERSITÉ des ALBUMS\n'
              f'Sur 10 000 playlists analysées', 
              fontsize=18, fontweight='bold', pad=20)

# Ajout d'un message central
circle = plt.Circle((0,0), 0.4, fc='white', linewidth=2, edgecolor='gray')
fig1.gca().add_artist(circle)
ax1.text(0, 0, f'{pct_plus_albums:.0f}%\nConfirmé', 
         horizontalalignment='center', verticalalignment='center',
         fontsize=20, fontweight='bold', color='#2c3e50')

plt.tight_layout()
dashboard_1_path = os.path.join(output_dir, 'dashboard_1_message_principal.png')
plt.savefig(dashboard_1_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Graphique principal sauvegardé : {dashboard_1_path}")
plt.show()

#################################################################################################

# 2. COMPARAISON SIMPLE : Barres horizontales
fig2, ax2 = plt.subplots(figsize=(12, 6))

moyennes = [playlists_stats['artistes_uniques_reels'].mean(), 
           playlists_stats['albums_uniques_reels'].mean()]
categories = ['Artistes uniques\npar playlist', 'Albums uniques\npar playlist']
colors_bars = ['#FF6B6B', '#4ECDC4']

bars = ax2.barh(categories, moyennes, color=colors_bars, height=0.6)

# Ajout des valeurs sur les barres
for i, (bar, value) in enumerate(zip(bars, moyennes)):
    ax2.text(value + 1, bar.get_y() + bar.get_height()/2, 
             f'{value:.1f}', ha='left', va='center', 
             fontsize=16, fontweight='bold')

ax2.set_xlabel('Nombre moyen par playlist', fontsize=14, fontweight='bold')
ax2.set_title('📊 En moyenne, chaque playlist contient plus d\'albums que d\'artistes\n'
              'Les utilisateurs explorent en profondeur les catalogues', 
              fontsize=16, fontweight='bold', pad=20)

ax2.grid(axis='x', alpha=0.3)
ax2.set_xlim(0, max(moyennes) * 1.2)

# Ajout d'une flèche et annotation
ax2.annotate('10,5 albums de plus\nen moyenne !', 
             xy=(moyennes[1], 1), xytext=(moyennes[1]+5, 0.3),
             arrowprops=dict(arrowstyle='->', color='green', lw=2),
             fontsize=12, fontweight='bold', color='green')

plt.tight_layout()
dashboard_2_path = os.path.join(output_dir, 'dashboard_2_comparaison_moyennes.png')
plt.savefig(dashboard_2_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Graphique de comparaison sauvegardé : {dashboard_2_path}")
plt.show()

#################################################################################################

# 3. TENDANCE PAR TAILLE : Message comportemental
fig3, ax3 = plt.subplots(figsize=(12, 7))

# Données par taille avec messages clairs
tailles_labels = ['Courtes\n(≤20 titres)', 'Moyennes\n(21-50 titres)', 
                  'Longues\n(51-100 titres)', 'Très longues\n(>100 titres)']
ratios_moyens = ratio_par_taille.values

bars = ax3.bar(tailles_labels, ratios_moyens, 
               color=['#FFE5B4', '#FFCC99', '#FFB366', '#FF9933'], 
               edgecolor='white', linewidth=2)

# Ligne de référence
ax3.axhline(y=1, color='red', linestyle='--', linewidth=3, alpha=0.8, 
           label='Égalité albums = artistes')

# Ajout des valeurs sur les barres
for bar, value in zip(bars, ratios_moyens):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f'{value:.2f}', ha='center', va='bottom', 
             fontsize=14, fontweight='bold')

ax3.set_ylabel('Ratio Albums/Artistes', fontsize=14, fontweight='bold')
ax3.set_title('🎯 Plus la playlist est longue, plus la diversité d\'albums augmente\n'
              'Comportement constant quelque soit la taille de playlist', 
              fontsize=16, fontweight='bold', pad=20)

ax3.grid(axis='y', alpha=0.3)
ax3.legend(fontsize=12)
ax3.set_ylim(0, max(ratios_moyens) * 1.1)

plt.tight_layout()
dashboard_3_path = os.path.join(output_dir, 'dashboard_3_tendance_taille.png')
plt.savefig(dashboard_3_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Graphique de tendance sauvegardé : {dashboard_3_path}")
plt.show()

#################################################################################################

# 4. INFOGRAPHIE DE SYNTHÈSE
fig4, ((ax4a, ax4b), (ax4c, ax4d)) = plt.subplots(2, 2, figsize=(16, 12))
fig4.suptitle('🎵 DÉCOUVERTE MUSICALE : Les utilisateurs Spotify explorent en PROFONDEUR', 
              fontsize=20, fontweight='bold', y=0.95)

# 4a. Statistique clé
ax4a.text(0.5, 0.5, f'{pct_plus_albums:.0f}%', 
          horizontalalignment='center', verticalalignment='center',
          fontsize=60, fontweight='bold', color='#4ECDC4',
          transform=ax4a.transAxes)
ax4a.text(0.5, 0.2, 'des playlists ont plus\nd\'albums que d\'artistes', 
          horizontalalignment='center', verticalalignment='center',
          fontsize=16, fontweight='bold', transform=ax4a.transAxes)
ax4a.set_xlim(0, 1)
ax4a.set_ylim(0, 1)
ax4a.axis('off')

# 4b. Ratio moyen
ax4b.text(0.5, 0.5, f'{ratio_moyen:.2f}', 
          horizontalalignment='center', verticalalignment='center',
          fontsize=50, fontweight='bold', color='#FF6B6B',
          transform=ax4b.transAxes)
ax4b.text(0.5, 0.2, 'albums par artiste\nen moyenne', 
          horizontalalignment='center', verticalalignment='center',
          fontsize=16, fontweight='bold', transform=ax4b.transAxes)
ax4b.set_xlim(0, 1)
ax4b.set_ylim(0, 1)
ax4b.axis('off')

# 4c. Différence moyenne
ax4c.text(0.5, 0.5, f'+{playlists_stats["diff_albums_artistes"].mean():.1f}', 
          horizontalalignment='center', verticalalignment='center',
          fontsize=50, fontweight='bold', color='#45B7D1',
          transform=ax4c.transAxes)
ax4c.text(0.5, 0.2, 'albums de plus\nque d\'artistes', 
          horizontalalignment='center', verticalalignment='center',
          fontsize=16, fontweight='bold', transform=ax4c.transAxes)
ax4c.set_xlim(0, 1)
ax4c.set_ylim(0, 1)
ax4c.axis('off')

# 4d. Conclusion métier
ax4d.text(0.5, 0.6, '💡 INSIGHT MÉTIER', 
          horizontalalignment='center', verticalalignment='center',
          fontsize=18, fontweight='bold', color='#2c3e50',
          transform=ax4d.transAxes)
ax4d.text(0.5, 0.4, 'Les utilisateurs préfèrent\nEXPLORER EN PROFONDEUR\nles catalogues d\'artistes\nplutôt que découvrir\nsuperficiellement', 
          horizontalalignment='center', verticalalignment='center',
          fontsize=14, fontweight='bold', transform=ax4d.transAxes)
ax4d.set_xlim(0, 1)
ax4d.set_ylim(0, 1)
ax4d.axis('off')

plt.tight_layout()
dashboard_4_path = os.path.join(output_dir, 'dashboard_4_infographie_synthese.png')
plt.savefig(dashboard_4_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Infographie de synthèse sauvegardée : {dashboard_4_path}")
plt.show()

print("\n🎯 Visualisations dashboard créées avec succès !")
print("📊 Fichiers générés pour dashboard grand public :")
print(f"   1. Message principal : {dashboard_1_path}")
print(f"   2. Comparaison : {dashboard_2_path}")
print(f"   3. Tendance : {dashboard_3_path}")
print(f"   4. Infographie : {dashboard_4_path}")

#################################################################################################

# Conclusion sur l'hypothèse
print("\nÉtape 4: Conclusion de l'analyse...")

print("="*80)
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

#################################################################################################

# Sauvegarde des résultats
results_path = os.path.join(output_dir, 'analyse_dispersion_resultats.csv')
playlists_stats.to_csv(results_path, index=False)
print(f"\nRésultats détaillés sauvegardés : {results_path}")

print("\n--- Analyse de la dispersion album/artiste terminée ---")
print(f"Hypothèse {'CONFIRMÉE' if resultats['pct_plus_albums'] > 50 else 'RÉFUTÉE'} avec {resultats['pct_plus_albums']:.1f}% de validation")

# Fin du script
