import re
import pandas as pd

ENTREE = "/mnt/c/Bioinfo_RAM/Data/metadata/ecoli_metadata.tsv"
SORTIE = "/mnt/c/Bioinfo_RAM/Data/metadata/ecoli_metadata_cat.tsv"

LABO = r"\blaborator|\blab (isolate|strain)|conjugation|experiment|\bmutant"
ALIMENT = r"\b(meat|beef|veal|pork|cheese|milk|food|sausages?|retail)\b"
HUMAIN = r"\b(homo sapiens|humans?|patients?|icu staff)\b"
PORC = r"\b(sus scrofa|pigs?|swine|porcine|piglets?)\b"
POULET = r"\b(gallus|chickens?|poultry|broilers?|hens?)\b"
BOVIN = r"\b(bos taurus|cows?|cattle|bovine|calf|calves|bulls?)\b"
CHIEN = r"\b(canis|dogs?|canine)\b"
SOURIS = r"\b(mus musculus|mouse|mice)\b"
ENV = r"\b(water|soil|river|sewage|seawater|lake|sediment|wastewater|wwtp|environment(al)?)\b"
NON_PRECISE = r"\b(urine|blood|stool|fec(es|e|al)|faec(es|al)|hospital|rectal swab|sputum|wound)\b"

REGLES_HOTE = [("humain", HUMAIN), ("porc", PORC), ("poulet", POULET),
               ("bovin", BOVIN), ("chien", CHIEN), ("souris", SOURIS)]
REGLES_SOURCE = ([("aliment", ALIMENT)] + REGLES_HOTE +
                 [("environnement", ENV), ("clinique/fèces non précisé", NON_PRECISE)])

def classer(texte, regles):
    for nom, motif in regles:
        if re.search(motif, texte, re.IGNORECASE):
            return nom
    return "autre"

def categorie(host, source):
    textes = [t for t in (host, source) if isinstance(t, str)]
    if any(re.search(LABO, t, re.IGNORECASE) for t in textes):
        return "laboratoire"
    for texte, regles in ((host, REGLES_HOTE), (source, REGLES_SOURCE)):
        if isinstance(texte, str):
            c = classer(texte, regles)
            if c != "autre":
                return c
    return "autre" if textes else "inconnu"

df = pd.read_csv(ENTREE, sep="\t")
df["categorie"] = [categorie(h, s) for h, s in zip(df["host"], df["isolation_source"])]
df.to_csv(SORTIE, sep="\t", index=False)

print(df["categorie"].value_counts())
autres = df[df["categorie"] == "autre"]
print()
print("Hôtes classés 'autre' :")
print(autres["host"].value_counts().head(10))
print()
print("Sources classées 'autre' :")
print(autres["isolation_source"].value_counts().head(15))
