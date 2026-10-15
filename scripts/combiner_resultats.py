import pandas as pd

R = "/mnt/c/Bioinfo_RAM/Results"
fichiers = {
    "K-12 MG1655": f"{R}/K12_amrfinder.tsv",
    "SE11": f"{R}/panel/GCF_000010385.1_ASM1038v1.tsv",
    "UTI89": f"{R}/panel/GCF_000013265.1_ASM1326v1.tsv",
    "SMS-3-5": f"{R}/panel/GCF_000019645.1_ASM1964v1.tsv",
    "ETEC H10407": f"{R}/panel/GCF_000210475.1_ASM21047v1.tsv",
}

tables = []
for souche, chemin in fichiers.items():
    df = pd.read_csv(chemin, sep="\t")
    df["Souche"] = souche
    tables.append(df)

tout = pd.concat(tables, ignore_index=True)
tout.to_csv(f"{R}/panel_amr_combine.tsv", sep="\t", index=False)

print("Détections par souche :")
print(tout["Souche"].value_counts().reindex(list(fichiers), fill_value=0))
print()
print("Détections par classe d'antibiotiques :")
print(pd.crosstab(tout["Class"], tout["Souche"]))
