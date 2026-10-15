import glob
import os
import pandas as pd

R = "/mnt/c/Bioinfo_RAM/Results/panel30"
META = "/mnt/c/Bioinfo_RAM/Data/metadata/panel30.tsv"
SORTIE = "/mnt/c/Bioinfo_RAM/Results/panel30_amr_combine.tsv"
SORTIE_RESUME = "/mnt/c/Bioinfo_RAM/Results/panel30_resume_par_genome.tsv"

meta = pd.read_csv(META, sep="\t")

tables = []
for chemin in sorted(glob.glob(f"{R}/*.tsv")):
    nom = os.path.basename(chemin)[:-4]
    accession = "_".join(nom.split("_")[:2])   # ex. GCF_001900675.1
    df = pd.read_csv(chemin, sep="\t")
    if len(df) > 0:
        df["accession"] = accession
        tables.append(df)

tout = pd.concat(tables, ignore_index=True)
tout = tout.merge(meta[["accession", "categorie"]], on="accession", how="left")
tout.to_csv(SORTIE, sep="\t", index=False)

# résumé par génome : les génomes SANS détection doivent rester dans le tableau
grp = tout.groupby("accession")
resume = pd.DataFrame({
    "n_detections": grp.size(),
    "n_classes": grp["Class"].nunique(),
    "n_acquis": grp["Subtype"].apply(lambda s: (s == "AMR").sum()),
    "n_mutations": grp["Subtype"].apply(lambda s: (s == "POINT").sum()),
})
resume = meta.set_index("accession")[["categorie"]].join(resume)
colonnes = ["n_detections", "n_classes", "n_acquis", "n_mutations"]
resume[colonnes] = resume[colonnes].fillna(0).astype(int)
resume = resume.sort_values(["categorie", "n_detections"])
resume.to_csv(SORTIE_RESUME, sep="\t")

print(len(tout), "détections au total")
print()
print(resume.to_string())
print()
par_cat = resume.groupby("categorie").agg(
    genomes=("n_detections", "size"),
    avec_detection=("n_detections", lambda s: int((s > 0).sum())),
    min_detections=("n_detections", "min"),
    mediane_detections=("n_detections", "median"),
    max_detections=("n_detections", "max"),
)
print(par_cat)
