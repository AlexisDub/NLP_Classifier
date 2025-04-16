# 🧠 NLP Classifier - League of Legends Region Prediction

Ce projet de NLP (traitement automatique du langage naturel) a pour objectif de prédire la **région** d’origine d’un **champion de League of Legends** à partir de son lore, de son rôle et de sa race. Le modèle s’appuie sur du machine learning et une vectorisation TF-IDF du texte.

---

## 🔧 Installation

1. Clone le repo :
   ```bash
   git clone <url_du_repo>
   cd nlp-lol-classifier
   ```

2. Crée un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate sous Windows
   ```

3. Installe les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Télécharge les stopwords français de NLTK :
   ```python
   import nltk
   nltk.download('stopwords')
   ```

---

## 📁 Structure du projet

```
├── data/                       # Données brutes des champions (.json)
│   └── fr_FR/champion/
├── output/                     # Données nettoyées générées automatiquement
├── generate_clean_dataset.py  # Génère les fichiers d'entraînement à partir des données brutes
├── remplacer_region.py        # Remplace les noms de régions dans le lore
├── remplacer_region_less_ionia.py
├── nlp_classifier.py          # Script principal d'entraînement et de prédiction
├── champions_region_role_race_template.json  # Métadonnées manuelles des champions
└── requirements.txt
```

---

## ⚙️ Fonctionnement

1. **Nettoyage & Préparation** :
   - `generate_clean_dataset.py` crée deux fichiers :
     - `champions_ready.json`
     - `champions_ready_less_ionia.json` (équilibré en limitant Ionia)

2. **Remplacement des régions dans le texte** :
   - `remplacer_region.py` / `remplacer_region_less_ionia.py` anonymisent les mentions de régions.

3. **Classification** :
   - `nlp_classifier.py` vectorise le texte avec TF-IDF et entraîne un classifieur `LogisticRegression`.

---

## 📊 Modèle utilisé

- Vectorisation : `TfidfVectorizer` avec stopwords français
- Classifieur : `LogisticRegression`
- Évaluation : `classification_report` + matrice de confusion avec `seaborn`

---

## 📌 À venir

- Amélioration du modèle avec des embeddings (spaCy, BERT)
- Ajout d’une interface interactive
- Prise en compte de versions multilingues

---

## 👨‍💻 Auteur

Projet académique sur le NLP appliqué à l’univers de League of Legends.
