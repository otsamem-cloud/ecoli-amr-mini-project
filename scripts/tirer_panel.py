import pandas as pd

ENTREE = "/mnt/c/Bioinfo_RAM/Data/metadata/ecoli_metadata_cat.tsv"
SORTIE = "/mnt/c/Bioinfo_RAM/Data/metadata/panel30.tsv"
LISTE = "/mnt/c/Bioinfo_RAM/Data/metadata/panel30_accessions.txt"

CATEGORIES = ["humain", "porc", "poulet", "bovin", "chien", "environnement"]
N_PAR_CATEGORIE = 5
GRAINE = 42

df = pd.read_csv(ENTREE, sep="\t")
candidats = df[df["categorie"].isin(CATEGORIES)]

panel = candidats.groupby("categorie").sample(n=N_PAR_CATEGORIE, random_state=GRAINE)
panel = panel.sort_values("categorie")

panel.to_csv(SORTIE, sep="\t", index=False)
panel["accession"].to_csv(LISTE, index=False, header=False)

pd.set_option("display.width", 250)
pd.set_option("display.max_colwidth", 28)
colonnes = ["accession", "categorie", "host", "isolation_source", "geo_loc_name", "collection_date"]
print(panel[colonnes].to_string(index=False))
