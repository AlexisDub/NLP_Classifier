## 📁 Dossier `output`

Ce dossier contient (ou contiendra) tous les datasets générés via les scripts suivants :

- `generate_clean_dataset.py`
- `remplacer_region.py`
- `remplacer_region_less_ionia.py` (à exécuter **après** `generate_clean_dataset.py`)

---

###  Si le dossier est vide

Lance le script `generate_clean_dataset.py`, qui va générer deux fichiers JSON :

- `champions_ready.json`  
  > Dataset contenant tous les personnages du jeu, à l’exception de quelques-uns sans région d’origine.

- `champions_ready_less_ionia.json`  
  > Version allégée du dataset précédent, sans 8 personnages originaires de la région **Ionia**, afin d’éviter un biais constaté.

---

###  Étapes suivantes

Une fois les deux fichiers JSON générés, tu peux exécuter :

- `remplacer_region.py`  
  ➜ Génère `champions_without_regions_in_description.json`  
  > Les mentions de régions sont supprimées des champs **"Origine/Histoire clé"**.

- `remplacer_region_less_ionia.py`  
  ➜ Génère `champions_less_ionia_without_regions_in_description.json`  
  > Même traitement, mais sur le dataset sans les personnages d’Ionia.

---

###  Tester les modèles

Tu peux ensuite tester `nlp_classifier.py` sur chacun de ces datasets pour comparer les résultats obtenus.

---

✨ Bon travail et bonnes expérimentations !
