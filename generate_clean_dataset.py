import os
import json
import random

# === CONFIGURATION ===
CHAMPION_FOLDER = os.path.join("data", "fr_FR", "champion")  # Dossier avec les .json des champions
FILLED_INFO_PATH = "champions_region_role_race_template.json"  # Fichier template 

# FICHIERS DE SORTIE
OUTPUT_PATH = "output/champions_ready.json" # Fichier de sortie avec toutes les infos
SECOND_OUTPUT_PATH = "output/champions_ready_less_ionia.json" # Fichier de sortie avec moins de champions d'Ionia


# === CHARGEMENT DU FICHIER RÉGION/RÔLE/RACE === 
with open(FILLED_INFO_PATH, "r", encoding="utf-8") as f:
    manual_info = json.load(f)



champions_exclus = ["AurelionSol","Fiddlesticks","Aatrox","Nocturne","Kindred","Alistar","Evelynn","Shaco","TahmKench","Ryze","Nami","Bard","Smolder","Belveth"]  # Liste des champions à exclure

# === RÉCUPÉRER LES FICHIERS JSON CHAMPIONS ===
champion_files = [f for f in os.listdir(CHAMPION_FOLDER) if f.endswith(".json")]
champion_names = [os.path.splitext(f)[0] for f in champion_files]

merged_dataset = []

for champ_name in sorted(champion_names): 

    if champ_name in champions_exclus:
        continue

    champ_path = os.path.join(CHAMPION_FOLDER, f"{champ_name}.json")
    
    with open(champ_path, "r", encoding="utf-8") as f:
        champ_json = json.load(f)
    
    champ_data = list(champ_json["data"].values())[0]
    tags = champ_data.get("tags", [])
    classe = tags[0] if len(tags) > 0 else "Inconnu"
    sous_classe = tags[1] if len(tags) > 1 else "Inconnue"
    partype = champ_data.get("partype", "Inconnu")
    difficulty = champ_data.get("info", {}).get("difficulty", "?")
    
    # Fusionner avec ton fichier manuel
    region = manual_info.get(champ_name, {}).get("Région", "Inconnue")
    role = manual_info.get(champ_name, {}).get("Rôle", "Inconnu")
    race = manual_info.get(champ_name, {}).get("Race", "Inconnue")

    merged_dataset.append({
        "Champion":champ_name,
        "Région": region,
        "Rôle": role,
        "Race": race,
        "Sous-classe": sous_classe,
        "Origine/Histoire clé": champ_data.get("lore", ""),
        "Style de jeu": f"{classe} avec {partype.lower()} comme ressource. Difficulté : {difficulty}",
        "Lien officiel": f"https://universe.leagueoflegends.com/fr_FR/champion/{champ_name.lower()}/",
    })

# === SUPPRESSION DU FICHIER DE SORTIE S'IL EXISTE ===
if os.path.exists(OUTPUT_PATH):
    os.remove(OUTPUT_PATH)


# === SAUVEGARDE
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(merged_dataset, f, ensure_ascii=False, indent=4)

print(f"{len(merged_dataset)} champions exportés dans {OUTPUT_PATH}")





# === EQUILIBRAGE : AUTRE FICHIER QUI CONTIENS MOINS DE PERSONNAGES VENANT DE LA REGION IONIA ===

# Sélectionner les champions dont la région est IONIA (on compare en majuscules pour être sûr)
champions_ionia = [champ for champ in merged_dataset if champ["Région"].upper() == "IONIA"]

# Choisir 14 champions aléatoirement parmi ceux d'Ionia, s'ils existent
champions_a_retirer = random.sample(champions_ionia, 8)


# Créer une nouvelle liste en retirant les champions sélectionnés
merged_dataset_less_ionia = [champ for champ in merged_dataset if champ not in champions_a_retirer]

# Sauvegarder le second fichier JSON
with open(SECOND_OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(merged_dataset_less_ionia, f, ensure_ascii=False, indent=4)

print(f"{len(merged_dataset_less_ionia)} champions exportés dans {SECOND_OUTPUT_PATH}")