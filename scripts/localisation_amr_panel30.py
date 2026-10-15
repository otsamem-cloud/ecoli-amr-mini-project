import pandas as pd

R = "/mnt/c/Bioinfo_RAM/Results"
tout = pd.read_csv(f"{R}/panel30_amr_combine.tsv", sep="\t")
contigs = pd.read_csv(f"{R}/panel30_contigs.tsv", sep="\t")
final = pd.read_csv(f"{R}/panel30_tableau_final.tsv", sep="\t")

amr = tout[tout["Type"] == "AMR"].copy()
amr = amr.merge(contigs[["accession", "contig", "type"]],
                left_on=["accession", "Contig id"],
                right_on=["accession", "contig"], how="left")

print("Détections AMR sans séquence correspondante :", int(amr["type"].isna().sum()), "sur", len(amr))
amr["type"] = amr["type"].fillna("inconnu")
print()

print("Localisation selon le sous-type :")
print(pd.crosstab(amr["Subtype"], amr["type"], margins=True).to_string())
print()

loc = pd.crosstab(amr["accession"], amr["type"])
for col in ["chromosome", "plasmide"]:
    if col not in loc.columns:
        loc[col] = 0
n_plasmides = contigs[contigs["type"] == "plasmide"].groupby("accession").size()
porteurs = amr[amr["type"] == "plasmide"].groupby("accession")["contig"].nunique()

tab = final[["accession", "categorie", "n_amr"]].set_index("accession")
tab = tab.join(loc[["chromosome", "plasmide"]].rename(
    columns={"chromosome": "amr_chromosome", "plasmide": "amr_plasmide"}))
tab = tab.join(n_plasmides.rename("n_plasmides")).join(porteurs.rename("plasmides_porteurs"))
tab = tab.fillna(0).astype(int, errors="ignore")
for c in ["amr_chromosome", "amr_plasmide", "n_plasmides", "plasmides_porteurs"]:
    tab[c] = tab[c].astype(int)
tab = tab.sort_values(["categorie", "n_amr"])
tab.to_csv(f"{R}/panel30_localisation_amr.tsv", sep="\t")

pd.set_option("display.width", 250)
print(tab.to_string())
