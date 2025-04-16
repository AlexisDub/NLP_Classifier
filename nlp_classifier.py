import os
import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords

# Téléchargement des stopwords si nécessaire
nltk.download('stopwords')

# Dictionnaire des descriptions pour chaque dataset
DATASET_DESCRIPTIONS = {
    "champions_ready.json": "Tous les personnages",
    "champions_ready_less_ionia.json": "Tous les personnages avec MOINS de personnages venant d'Ionia",
    "champions_without_regions_in_description.json": "Tous les personnages SANS noms de régions dans les histoires",
    "champions_less_ionia_without_regions_in_description.json": "Tous les personnages SANS noms de régions dans les histoires avec MOINS de personnages venant d'Ionia",
}


def choose_dataset(output_dir="output"):
    # Liste des fichiers .json dans le dossier output
    files = sorted([f for f in os.listdir(output_dir) if f.endswith('.json')])
    if not files:
        raise FileNotFoundError(f"Aucun fichier .json trouvé dans le dossier '{output_dir}'")

    # Affichage des choix disponibles
    print("Jeu de données disponibles :")
    for idx, fname in enumerate(files, 1):
        desc = DATASET_DESCRIPTIONS.get(fname, "")
        print(f"  {idx}. {fname} -> {desc}")

    # Sélection utilisateur
    choice = None
    while choice not in range(1, len(files) + 1):
        try:
            choice = int(input(f"Sélectionnez un dataset [1-{len(files)}] : "))
        except ValueError:
            continue

    selected = files[choice - 1]
    print(f"Dataset sélectionné : {selected} -> {DATASET_DESCRIPTIONS.get(selected, '')}\n")
    return os.path.join(output_dir, selected)


def clean_text(text):
    """Nettoyage basique du texte"""
    return text.lower()


def main():
    # 1. Choix et chargement des données
    dataset_path = choose_dataset()
    dataset_name = os.path.basename(dataset_path)
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)

    # 2. Concaténation des champs texte
    df["all_features_text"] = (
        df["Origine/Histoire clé"] + " " +
        df["Race"] + " " +
        df["Rôle"]
    )
    df["clean_all_features_text"] = df["all_features_text"].apply(clean_text)

    # 3. Vectorisation TF-IDF
    stop_words_fr = stopwords.words('french')
    tfidf = TfidfVectorizer(max_features=1000, stop_words=stop_words_fr)
    X = tfidf.fit_transform(df["clean_all_features_text"])

    # 4. Définition de la cible
    y = df["Région"]

    # 5. Séparation train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, stratify=y, test_size=0.3, random_state=42
    )

    # 6. Entraînement du modèle
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # 7. Évaluation
    y_pred = model.predict(X_test)
    print(f"\n--- Résultats pour le dataset '{dataset_name}' ---")
    print(classification_report(y_test, y_pred))

    # 8. Affichage de la matrice de confusion
    plt.figure(figsize=(10, 6))
    conf_matrix = pd.crosstab(y_test, y_pred, rownames=["Vrai"], colnames=["Prédit"])
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues")
    plt.title(f"Matrice de confusion ({dataset_name})")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
