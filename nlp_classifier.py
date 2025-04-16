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
nltk.download('stopwords')


# === 1. CHARGEMENT DES DONNES : CHOISIR SUR QUEL SET DE DONNEES LANCER ===


#-----------------   AVEC le nom des régions mentionnnés quelques fois dans les histoires des personnages --------------------

#Fichier qui contient les champions et leurs caractéristiques
# with open("output/champions_ready.json", "r", encoding="utf-8") as f:
#      data = json.load(f)

#Fichier qui contient les champions et leurs caractéristiques MAIS avec MOINS de personnages provenant de la région Ionia (pour éviter le biais de la région Ionia)
with open("output/champions_ready_less_ionia.json", "r", encoding="utf-8") as f:
      data = json.load(f)


#-----------------   SANS le nom des régions mentionnnés quelques fois dans les histoires des personnages -------------------

#Fichier qui contient les champions et leurs caractéristiques
#with open("output/champions_without_regions_in_description.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

#Fichier qui contient les champions et leurs caractéristiques MAIS avec MOINS de personnages provenant de la région Ionia (pour éviter le biais de la région Ionia)
#with open("output/champions_less_ionia_without_regions_in_description.json", "r", encoding="utf-8") as f:
#     data = json.load(f)




# Transformation en DataFrame
df = pd.DataFrame(data)

# === 2. Création d'une nouvelle colonne "all_features_text" ===
# On concatène le lore, le rôle et la race pour enrichir le texte
df["all_features_text"] = (
    df["Origine/Histoire clé"] + " " +
    df["Race"] + " " +
    df["Rôle"]



)

# Fonction de nettoyage des textes
def clean_text(text):
    text = text.lower()
    return text

# On applique le nettoyage sur la nouvelle colonne
df["clean_all_features_text"] = df["all_features_text"].apply(clean_text)

# === 3. Vectorisation TF-IDF ===
stop_words_fr = stopwords.words('french')
tfidf = TfidfVectorizer(max_features=1000, stop_words=stop_words_fr)
X = tfidf.fit_transform(df["clean_all_features_text"])

# === 4. Définition de la cible : ici, la Région ===
y = df["Région"]

# === 5. Séparation des données en jeu d'entraînement et de test ===
# Vous pouvez modifier ici le ratio, par exemple test_size=0.35 pour 65% d'entraînement
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.3, random_state=42
)

# === 6. Entraînement du modèle ===
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# === 7. Prédiction et évaluation ===
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# === 8. Visualisation de la matrice de confusion ===
plt.figure(figsize=(10, 6))
conf_matrix = pd.crosstab(y_test, y_pred, rownames=["Vrai"], colnames=["Prédit"])
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues")
plt.title("Matrice de confusion - Prédiction des Régions")
plt.tight_layout()
plt.show()
