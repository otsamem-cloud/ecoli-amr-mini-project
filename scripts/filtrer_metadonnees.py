import json
import pandas as pd

FICHIER = "/mnt/c/Bioinfo_RAM/Data/metadata/ecoli_complete_refseq.jsonl"
SORTIE = "/mnt/c/Bioinfo_RAM/Data/metadata/ecoli_metadata.tsv"
CHAMPS = ["isolation_source", "host", "geo_loc_name", "collection_date"]
VIDES = {"", "missing", "not applicable", "not collected", "not provided",
         "na", "n/a", "unknown", "none", "restricted access"}

def nettoyer(valeur):
    """Transforme les valeurs 'vides' (missing, NA...) en None."""
    if valeur is None:
        return None
    texte = str(valeur).strip()
    bas = texte.lower()
    if bas in VIDES or bas.startswith(("na(", "missing", "not ")):
        return None
    return texte

lignes = []
for ligne in open(FICHIER):
    d = json.loads(ligne)
    attributs = d.get("assembly_info", {}).get("biosample", {}).get("attributes", [])
    attr = {a.get("name"): a.get("value") for a in attributs}
    resume = {
        "accession": d.get("accession"),
        "organism": d.get("organism", {}).get("organism_name"),
        "strain": attr.get("strain"),
    }
    for champ in CHAMPS:
        resume[champ] = nettoyer(attr.get(champ))
    lignes.append(resume)

df = pd.DataFrame(lignes)
df.to_csv(SORTIE, sep="\t", index=False)

print(len(df), "génomes")
print()
print("Champs réellement renseignés (après nettoyage) :")
print(df[CHAMPS].notna().sum())
print()
renseignes = (df["host"].notna() | df["isolation_source"].notna()).sum()
print("Génomes avec host OU isolation_source :", renseignes)
print()
print("Valeurs les plus fréquentes de host :")
print(df["host"].value_counts().head(10))
