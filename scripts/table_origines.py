import json
import pandas as pd

FICHIER = "/mnt/c/Bioinfo_RAM/Data/metadata/ecoli_test20.jsonl"
CHAMPS = ["isolation_source", "host", "geo_loc_name", "collection_date"]

lignes = []
for ligne in open(FICHIER):
    d = json.loads(ligne)
    attributs = d.get("assembly_info", {}).get("biosample", {}).get("attributes", [])
    attr = {a["name"]: a["value"] for a in attributs}
    resume = {"accession": d.get("accession"), "strain": attr.get("strain")}
    for champ in CHAMPS:
        resume[champ] = attr.get(champ)
    lignes.append(resume)

df = pd.DataFrame(lignes)
pd.set_option("display.width", 250)
pd.set_option("display.max_colwidth", 35)
print(df.to_string())
