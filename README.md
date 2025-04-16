# Projet NLP sur les Champions de League of Legends

Ce projet vise à générer et classifier un jeu de données complet sur les champions de League of Legends. Le pipeline s’appuie sur un fichier de template manuel contenant les informations essentielles (Région, Rôle, Race) pour chaque champion, qui est ensuite fusionné avec des données complémentaires extraites des fichiers JSON individuels des champions.

## Table des matières

- [Structure du Projet](#structure-du-projet)
- [Mode d’Emploi](#mode-demploi)
- [Scripts Principaux](#scripts-principaux)
- [Choix et Considérations](#choix-et-considérations)
- [Installation des Dépendances](#installation-des-dépendances)
- [Licence](#licence)

## Structure du Projet

- **champions_region_role_race_template.json**  
  Ce fichier, élaboré manuellement à partir du site officiel de League of Legends, liste pour chaque champion les attributs suivants :
  - **Région**
  - **Rôle**
  - **Race**

  Certains champions (ex. : Fiddlesticks, Aatrox, Nocturne, Kindred, Alistar, Evelynn, Shaco, Tahm Kench, Ryze, Nami, Bard, Smolder, Aurelion, etc.) ont été intentionnellement exclus car ils n'ont pas de véritable région d'origine.

- **generate_clean_dataset.py**  
  Ce script parcourt le dossier `data/fr_FR/champion/` contenant les fichiers JSON individuels. Il fusionne les informations extraites (lore, tags, type de ressource, difficulté, etc.) avec le fichier de template manuel pour créer un jeu de données complet. Pour chaque champion, le jeu de données contient les champs suivants :
  - **Champion**
  - **Région**
  - **Rôle**
  - **Race**
  - **Sous-classe**
  - **Origine/Histoire clé** (le lore récupéré depuis le JSON du champion)
  - **Style de jeu** (décrit par le type de champion, sa ressource et sa difficulté)
  - **Lien officiel** (vers la page du champion sur l’univers League of Legends)

  Deux fichiers de sortie sont générés :
  - `champions_ready.json` : le dataset complet.
  - `champions_ready_less_ionia.json` : une version équilibrée avec 8 champions de la région Ionia retirés aléatoirement afin de réduire un biais potentiel.

- **nlp_classifier.py**  
  Ce script entraîne un modèle de classification NLP pour prédire la région d’un champion à partir d’un texte concaténé constitué du lore, de la Race et du Rôle. Les étapes principales incluent :
  1. Conversion du JSON en DataFrame Pandas.
  2. Concatenation des champs textuels pour créer une colonne enrichie.
  3. Nettoyage du texte (mise en minuscules, etc.).
  4. Vectorisation par TF-IDF (en utilisant les stop words en français avec NLTK).
  5. Séparation des données en ensembles d'entraînement et de test (stratification incluse).
  6. Entraînement d’un modèle de régression logistique.
  7. Évaluation avec un rapport de classification et visualisation d’une matrice de confusion via Seaborn.

- **remplacer_region.py et remplacer_region_less_ionia.py**  
  Ces scripts remplacent les mentions explicites des noms de région dans le champ **Origine/Histoire clé** par le marqueur générique `[region]`.  
  Le processus est le suivant :
  1. Une liste prédéfinie de noms de régions (ex. : Bandle, Bilgewater, Demacia, Freljord, Ionia, Ixtal, Void, Néant, Noxus, Piltover, Shurima, Targon, Zaun, Îles Obscures) est définie.
  2. Les noms sont triés par ordre de longueur décroissante pour éviter les correspondances erronées.
  3. Une expression régulière (regex) est construite pour détecter précisément ces noms.
  4. Chaque occurrence dans le champ **Origine/Histoire clé** est remplacée par `[region]`.
  5. Le résultat est sauvegardé dans un nouveau fichier JSON :
     - `champions_without_regions_in_description.json` (pour le dataset complet)
     - `champions_less_ionia_without_regions_in_description.json` (pour le dataset moins biaisé par Ionia)

## Mode d’Emploi

1. **Installation**  
   Installez les dépendances à l’aide du fichier `requirements.txt` :
   ```bash
   pip install -r requirements.txt

## Génération du jeu de données

- Lance le script `generate_clean_dataset.py`. Celui-ci traitera les fichiers JSON situés dans le dossier `data/fr_FR/champion/` et générera deux jeux de données :
  - **champions_ready.json** (jeu complet)
  - **champions_ready_less_ionia.json** (jeu équilibré en retirant 8 champions de la région Ionia)

## Classification NLP

- Exécute `nlp_classifier.py` pour entraîner un modèle de régression logistique qui classifie les champions par leur région à partir du texte fusionné (concaténation du lore, de la Race et du Rôle).
- Le script affiche :
  - Un rapport de classification
  - Une matrice de confusion, facilitant la visualisation rapide des erreurs de classification et l’identification des confusions entre les régions.

## Remplacement des noms de régions

- Selon le jeu de données utilisé, lance l’un des scripts suivants pour remplacer les noms de région dans le champ **Origine/Histoire clé** par `[region]` :
  - Pour le jeu complet : exécute `remplacer_region.py`
  - Pour le jeu « moins Ionia » : exécute `remplacer_region_less_ionia.py`
- Ces scripts créent de nouveaux fichiers JSON avec les descriptions nettoyées.

## Choix et Considérations

- **Exclusion de certains champions :**  
  Le fichier manuel de template a été élaboré en omettant certains champions (ex. : Fiddlesticks, Aatrox, Nocturne, etc.) qui ne disposent pas d’une région d’origine cohérente. Cela permet de concentrer l’analyse sur des entrées plus précises.

- **Équilibrage du dataset :**  
  Le retrait aléatoire de 8 champions de la région Ionia dans le fichier `champions_ready_less_ionia.json` vise à réduire un biais perceptible dans la répartition des régions lors de l’apprentissage du modèle NLP.

- **Nettoyage des textes :**  
  La concaténation de plusieurs champs textuels (lore, Race, Rôle) permet d’enrichir la représentation textuelle et d’améliorer la qualité de la vectorisation TF-IDF. Le choix du TfidfVectorizer et l’utilisation de stop words français via NLTK ont été retenus afin d’adapter l’analyse aux spécificités linguistiques.

- **Visualisation de la performance :**  
  L’utilisation de la matrice de confusion et de Seaborn permet de visualiser rapidement les erreurs de classification et d’identifier d’éventuelles confusions entre les régions.

## Conclusion

Ce projet combine :

- **L’extraction et l’enrichissement de données** à partir de sources JSON et d’un template manuel,
- **Le nettoyage textuel** à l’aide d’expressions régulières,
- **Une approche de classification NLP** via scikit-learn.

Les différentes étapes (génération du dataset, classification et nettoyage) offrent un pipeline complet pour explorer, équilibrer et analyser des données narratives sur les champions de League of Legends.

