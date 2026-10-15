import pandas as pd

df = pd.read_csv("/mnt/c/Bioinfo_RAM/Data/metadata/ecoli_metadata_cat.tsv", sep="\t")
sans_hote = df[(df["categorie"] == "autre") & (df["host"].isna())]

print(len(sans_hote), "génomes 'autre' sans host")
print()
print(sans_hote["isolation_source"].value_counts().head(25))
