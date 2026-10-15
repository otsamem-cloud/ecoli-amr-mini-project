import pandas as pd

R = "/mnt/c/Bioinfo_RAM/Results"
tout = pd.read_csv(f"{R}/panel30_amr_combine.tsv", sep="\t")
contigs = pd.read_csv(f"{R}/panel30_contigs.tsv", sep="\t")
final = pd.read_csv(f"{R}/panel30_tableau_final.tsv", sep="\t")

acquis = tout[(tout["Type"] == "AMR") & (tout["Subtype"] == "AMR")]
acquis = acquis.merge(contigs[["accession", "contig", "type"]],
                      left_on=["accession", "Contig id"],
                      right_on=["accession", "contig"], how="left")
chrom = acquis[acquis["type"] == "chromosome"]

res = chrom.groupby("accession").agg(
    n_genes=("Element symbol", "size"),
    debut=("Start", "min"),
    fin=("Stop", "max"),
)
res["etendue_kb"] = ((res["fin"] - res["debut"]) / 1000).round(1)
taille = contigs[contigs["type"] == "chromosome"].set_index("accession")["longueur"]
res["chromosome_Mb"] = (taille / 1e6).round(2)
res = res.join(final.set_index("accession")["categorie"])
res = res.sort_values("n_genes", ascending=False)
print(res.to_string())
