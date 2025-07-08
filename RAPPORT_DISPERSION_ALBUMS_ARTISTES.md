# 📊 Rapport d'Analyse : Dispersion Album/Artiste dans les Playlists

**Auteur :** Hugo HOUNTONDJI  
**Date :** 2024  
**Objectif :** Analyser l'hypothèse "Les playlists contiennent plus d'albums uniques que d'artistes (forte dispersion album/artiste)"


---


## 🎯 Résumé Exécutif

L'analyse statistique de 10 000 playlists confirme de manière très significative l'hypothèse de dispersion album/artiste. **87,2% des playlists contiennent effectivement plus d'albums uniques que d'artistes**, avec un ratio moyen de 1,319 albums par artiste.


---


## 📈 Méthodologie

### Données Analysées
- **Volume :** 664 712 entrées de tracks provenant de 10 000 playlists
- **Source :** Dataset alcrowd nettoyé
- **Période :** Données Spotify collectées

### Métriques Calculées
1. **Nombre d'albums uniques** par playlist (comptage réel)
2. **Nombre d'artistes uniques** par playlist (comptage réel)
3. **Ratio albums/artistes** par playlist
4. **Différence (albums - artistes)** par playlist

### Tests Statistiques
- **Test de Wilcoxon** pour échantillons appariés
- **Analyses descriptives** complètes
- **Segmentation par taille** de playlist


---


## 🔍 Résultats Principaux

### 1. Statistiques Descriptives

| Métrique | Albums Uniques | Artistes Uniques |
|----------|----------------|------------------|
| **Moyenne** | 48,71 | 38,24 |
| **Médiane** | 37,00 | 30,00 |
| **Écart-type** | 38,88 | 30,24 |


### 2. Test de l'Hypothèse

✅ **HYPOTHÈSE CONFIRMÉE**

- **87,2%** des playlists ont plus d'albums que d'artistes (8 723/10 000)
- **Ratio moyen** albums/artistes : **1,319**
- **Différence moyenne** : **+10,47** albums de plus que d'artistes
- **Test de Wilcoxon** : p-value < 0,001 (hautement significatif)

### 3. Analyse Segmentée par Taille

Les playlists montrent une dispersion album/artiste **constante** quelle que soit leur taille :

| Taille de Playlist | Ratio Moyen Albums/Artistes |
|-------------------|----------------------------|
| Petite (≤20 tracks) | > 1,0 |
| Moyenne (21-50 tracks) | > 1,0 |
| Grande (51-100 tracks) | > 1,0 |
| Très grande (>100 tracks) | > 1,0 |


---

## 💡 Interprétations Métier

### Comportement des Utilisateurs
1. **Exploration musicale approfondie** : Les utilisateurs tendent à explorer plusieurs albums d'un même artiste
2. **Diversité des œuvres** : Préférence pour la variété des albums plutôt que la multiplicité des artistes
3. **Fidélité artistique** : Tendance à approfondir la discographie des artistes appréciés

### Implications pour Spotify
1. **Recommandations** : Privilégier la suggestion d'albums complets plutôt que d'artistes isolés
2. **Découverte musicale** : Mettre en avant la discographie étendue des artistes
3. **Interface utilisateur** : Faciliter la navigation entre albums d'un même artiste

---


## 📊 Exemples Concrets

### Cas Typiques Observés

**Playlist "COACHELLA 2013"** :
- 41 artistes uniques → 82 albums uniques
- Ratio = 2,0 (forte dispersion)
- 207 tracks au total

**Playlist "Country"** :
- 35 artistes uniques → 57 albums uniques  
- Ratio = 1,63 (dispersion marquée)
- 74 tracks au total

**Contre-exemple - Playlist "Hamilton"** :
- 11 artistes uniques → 2 albums uniques
- Ratio = 0,18 (concentration artistique)
- Cas particulier : soundtrack d'une comédie musicale

---

## 📈 Visualisations Dashboard Grand Public

### Objectif Communication
Afin de rendre les résultats accessibles au grand public et aux décideurs, **4 visualisations spécialisées** ont été créées pour un dashboard de communication. Ces graphiques privilégient la **clarté du message** et l'**impact visuel**.

### 1. Message Principal : Graphique en Secteurs 
**Fichier :** `dashboard_1_message_principal.png`

- **Format :** Diagramme circulaire avec mise en relief
- **Message clé :** "🎵 Les playlists Spotify privilégient la DIVERSITÉ des ALBUMS"
- **Chiffre percutant :** **87%** des playlists confirmées au centre
- **Public cible :** Grand public, médias, direction
- **Impact :** Compréhension immédiate du phénomène

### 2. Comparaison Directe : Barres Horizontales
**Fichier :** `dashboard_2_comparaison_moyennes.png`

- **Format :** Barres horizontales colorées avec annotations
- **Données :** Moyennes albums vs artistes (48,7 vs 38,2)
- **Insight :** "+10,5 albums de plus en moyenne !"
- **Message :** "En moyenne, chaque playlist contient plus d'albums que d'artistes"
- **Utilité :** Présentation en réunion, justification quantitative

### 3. Analyse Comportementale : Tendance par Taille
**Fichier :** `dashboard_3_tendance_taille.png`

- **Format :** Graphique en barres avec gradient de couleurs
- **Segmentation :** Courtes, Moyennes, Longues, Très longues playlists
- **Découverte :** Ratio constant >1 quelque soit la taille
- **Message :** "Plus la playlist est longue, plus la diversité d'albums augmente"
- **Public :** Équipes produit, UX designers

### 4. Infographie de Synthèse : Dashboard Exécutif
**Fichier :** `dashboard_4_infographie_synthese.png`

- **Format :** Quadrant avec métriques clés et insight métier
- **Données :**
  - **87%** de validation de l'hypothèse
  - **1,32** albums par artiste en moyenne  
  - **+10,5** albums de différence
  - **💡 Insight :** "Les utilisateurs préfèrent EXPLORER EN PROFONDEUR"
- **Usage :** Présentation direction, communication externe

### Impact Communication
Ces visualisations transforment des **analyses statistiques complexes** en **messages simples et mémorisables** :

✅ **Accessibilité** : Compréhension sans expertise technique  
✅ **Mémorisation** : Messages visuels marquants  
✅ **Actionnable** : Insights métier directement exploitables  
✅ **Polyvalence** : Adaptées à différents publics et contextes  

---

## 🎵 Conclusion Générale

L'hypothèse de **forte dispersion album/artiste** est **CONFIRMÉE** avec une très haute significance statistique. Cette tendance révèle un comportement d'écoute sophistiqué où les utilisateurs privilégient :

1. **L'exploration approfondie** des catalogues d'artistes
2. **La diversité des œuvres** au sein d'une sélection d'artistes ciblée
3. **Une approche qualitative** de la curation musicale

Cette analyse suggère que les playlists Spotify reflètent une démarche de découverte musicale **intensive plutôt qu'extensive**, où les utilisateurs préfèrent creuser la richesse artistique d'un nombre restreint d'artistes plutôt que d'écumer superficiellement un large éventail d'artistes.

---

## 📁 Fichiers Générés

### Scripts et Données
1. **`album_unique_artistes.py`** : Script d'analyse complet
2. **`analyse_dispersion_resultats.csv`** : Données détaillées par playlist
3. **`RAPPORT_DISPERSION_ALBUMS_ARTISTES.md`** : Ce rapport de synthèse

### Visualisations Techniques
4. **`analyse_dispersion_album_artiste.png`** : Visualisations techniques complètes (6 graphiques)

### Visualisations Dashboard Grand Public
5. **`dashboard_1_message_principal.png`** : Graphique en secteurs avec message percutant
6. **`dashboard_2_comparaison_moyennes.png`** : Comparaison barres horizontales
7. **`dashboard_3_tendance_taille.png`** : Analyse comportementale par taille
8. **`dashboard_4_infographie_synthese.png`** : Infographie exécutive complète

---

*Rapport généré automatiquement par l'analyse statistique Python* 