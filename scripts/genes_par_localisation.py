import pandas as pd

R = "/mnt/c/Bioinfo_RAM/Results"
tout = pd.read_csv(f"{R}/panel30_amr_combine.tsv", sep="\t")
contigs = pd.read_csv(f"{R}/panel30_contigs.tsv", sep="\t")

acquis = tout[(tout["Type"] == "AMR") & (tout["Subtype"] == "AMR")]
acquis = acquis.merge(contigs[["accession", "contig", "type"]],
                      left_on=["accession", "Contig id"],
                      right_on=["accession", "contig"], how="left")

for localisation in ["chromosome", "plasmide"]:
    sel = acquis[acquis["type"] == localisation]
    print(f"== {localisation} : {len(sel)} détections dans {sel['accession'].nunique()} génomes")
    print("Scope :", sel["Scope"].value_counts().to_dict())
    print(sel["Element symbol"].value_counts().head(15).to_string())
    print()
