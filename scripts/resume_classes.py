import pandas as pd

R = "/mnt/c/Bioinfo_RAM/Results"
souches = ["K-12 MG1655", "SE11", "UTI89", "SMS-3-5", "ETEC H10407"]

tout = pd.read_csv(f"{R}/panel_amr_combine.tsv", sep="\t")

# 1 = au moins une détection dans la classe, 0 = aucune
presence = (pd.crosstab(tout["Class"], tout["Souche"]) > 0).astype(int)
presence = presence.reindex(columns=souches, fill_value=0)

print(presence)
print()
print("Nombre de classes touchées par souche :")
print(presence.sum())
