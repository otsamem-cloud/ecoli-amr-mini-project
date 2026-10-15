import glob
import os
import pandas as pd
from Bio import SeqIO

DATA = "/mnt/c/Bioinfo_RAM/Data/panel30/ncbi_dataset/data"
SORTIE = "/mnt/c/Bioinfo_RAM/Results/panel30_contigs.tsv"

lignes = []
for chemin in sorted(glob.glob(f"{DATA}/GCF_*/*_genomic.fna")):
    accession = "_".join(os.path.basename(chemin).split("_")[:2])
    for rec in SeqIO.parse(chemin, "fasta"):
        type_ = "plasmide" if "plasmid" in rec.description.lower() else "chromosome"
        lignes.append({"accession": accession, "contig": rec.id,
                       "longueur": len(rec.seq), "type": type_,
                       "description": rec.description})

df = pd.DataFrame(lignes)
df.to_csv(SORTIE, sep="\t", index=False)

resume = df.groupby("accession").agg(
    n_contigs=("contig", "size"),
    n_chromosomes=("type", lambda s: int((s == "chromosome").sum())),
    n_plasmides=("type", lambda s: int((s == "plasmide").sum())),
    taille_totale_Mb=("longueur", lambda s: round(s.sum() / 1e6, 2)),
)
pd.set_option("display.width", 250)
pd.set_option("display.max_colwidth", 90)
print(resume.to_string())
print()

suspects = df[((df["type"] == "chromosome") & ((df["longueur"] < 1_000_000) | (df["longueur"] > 7_000_000)))
              | ((df["type"] == "plasmide") & (df["longueur"] > 1_000_000))]
print("Séquences à vérifier (taille incohérente avec le type) :", len(suspects))
print(suspects[["accession", "contig", "longueur", "type", "description"]].to_string(index=False))
print()
print("Génomes dont le nombre de chromosomes n'est pas 1 :", list(resume[resume["n_chromosomes"] != 1].index))
