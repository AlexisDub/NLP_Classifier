import json
import re

# Liste des noms de régions à remplacer
regions = [
    "Bandle", "Bandle City", "Bilgewater", "Demacia", "Freljord", 
    "Ionia", "Ixtal", "Void", "Néant", "Noxus", 
    "Piltover", "Shurima", "Targon", "Zaun", "Îles Obscures"
]

# Pour éviter des conflits dans le matching, trions par longueur décroissante
regions_sorted = sorted(regions, key=len, reverse=True)
# Création d'un pattern regex qui match l'un des noms de région, en prenant soin des bornes de mots
pattern = r'\b(?:' + '|'.join(map(re.escape, regions_sorted)) + r')\b'

def remplacer_regions(texte):
    return re.sub(pattern, "[region]", texte)

# Chargement du fichier JSON (par exemple "champions.json")
with open("output/champions_ready_less_ionia.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Parcourir chaque champion et modifier le champ "Origine/Histoire clé"
for champion in data:
    if "Origine/Histoire clé" in champion:
        champion["Origine/Histoire clé"] = remplacer_regions(champion["Origine/Histoire clé"])

# Sauvegarder le résultat dans un nouveau fichier (par exemple "champions_modifié.json")
with open("output/champions_less_ionia_without_regions_in_description.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
