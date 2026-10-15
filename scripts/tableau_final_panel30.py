import os
import pandas as pd

R = "/mnt/c/Bioinfo_RAM/Results"
meta = pd.read_csv("/mnt/c/Bioinfo_RAM/Data/metadata/panel30.tsv", sep="\t")
resume = pd.read_csv(f"{R}/panel30_resume_par_genome.tsv", sep="\t")

lignes = []
for ligne in open(f"{R}/panel30_mlst.tsv"):
    champs = ligne.rstrip("\n").split("\t")
    nom = os.path.basename(champs[0])
    accession = "_".join(nom.split("_")[:2])
    st, alleles = champs[2], champs[3:]
    if st != "-":
        remarque = ""
    elif any("(-)" in a for a in alleles):
        remarque = "gène non trouvé"
    elif any("~" in a for a in alleles):
        remarque = "allèle nouveau"
    else:
        remarque = "profil non répertorié"
    lignes.append({"accession": accession, "ST": "" if st == "-" else st, "ST_remarque": remarque})

mlst = pd.DataFrame(lignes)
colonnes_meta = ["accession", "categorie", "host", "isolation_source", "geo_loc_name", "collection_date"]
colonnes_amr = ["accession", "n_amr", "n_classes", "n_acquis", "n_mutations", "n_disrupt", "n_stress"]

final = (meta[colonnes_meta]
         .merge(mlst, on="accession", how="left")
         .merge(resume[colonnes_amr], on="accession", how="left")
         .sort_values(["categorie", "n_amr"]))
final.to_csv(f"{R}/panel30_tableau_final.tsv", sep="\t", index=False)

pd.set_option("display.width", 250)
pd.set_option("display.max_colwidth", 22)
affichage = ["accession", "categorie", "geo_loc_name", "ST", "ST_remarque", "n_amr", "n_classes", "n_acquis", "n_mutations"]
print(final[affichage].to_string(index=False))
