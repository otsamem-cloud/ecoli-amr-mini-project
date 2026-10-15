import json
import collections

FICHIER = "/mnt/c/Bioinfo_RAM/Data/metadata/ecoli_test20.jsonl"

compteur = collections.Counter()
n = 0
for ligne in open(FICHIER):
    d = json.loads(ligne)
    n += 1
    attributs = d.get("assembly_info", {}).get("biosample", {}).get("attributes", [])
    compteur.update({a["name"] for a in attributs})

print(n, "génomes")
for nom, k in compteur.most_common(15):
    print(k, nom)
