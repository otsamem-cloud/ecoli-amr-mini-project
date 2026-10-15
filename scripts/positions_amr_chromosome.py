import pandas as pd

R = "/mnt/c/Bioinfo_RAM/Results"
tout = pd.read_csv(f"{R}/panel30_amr_combine.tsv", sep="\t")
contigs = pd.read_csv(f"{R}/panel30_contigs.tsv", sep="\t")

acquis = tout[(tout["Type"] == "AMR") & (tout["Subtype"] == "AMR")]
acquis = acquis.merge(contigs[["accession", "contig", "type"]],
                      left_on=["accession", "Contig id"],
                      right_on=["accession", "contig"], how="left")
chrom = acquis[acquis["type"] == "chromosome"]

CIBLES = ["GCF_029625135.1", "GCF_988243845.1", "GCF_024585985.1",
          "GCF_059727225.1", "GCF_024585365.1"]
for acc in CIBLES:
    sel = chrom[chrom["accession"] == acc].sort_values("Start")
    sel = sel.assign(ecart_kb=(sel["Start"] - sel["Stop"].shift()).div(1000).round(1))
    print(f"== {acc} ({len(sel)} gènes)")
    print(sel[["Element symbol", "Start", "Stop", "Strand", "ecart_kb"]].to_string(index=False))
    print()
