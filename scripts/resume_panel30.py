import pandas as pd

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", None)

R = "/mnt/c/Bioinfo_RAM/Results"
tout = pd.read_csv(f"{R}/panel30_amr_combine.tsv", sep="\t")
meta = pd.read_csv("/mnt/c/Bioinfo_RAM/Data/metadata/panel30.tsv", sep="\t")

for sous_type in ["BIOCIDE", "POINT_DISRUPT"]:
    sel = tout[tout["Subtype"] == sous_type]
    print(f"{sous_type} ({len(sel)} lignes) :")
    print(sel["Element symbol"].value_counts().to_string())
    print()

amr = tout[tout["Type"] == "AMR"]
grp = amr.groupby("accession")
resume = pd.DataFrame({
    "n_amr": grp.size(),
    "n_classes": grp["Class"].nunique(),
    "n_acquis": grp["Subtype"].apply(lambda s: (s == "AMR").sum()),
    "n_mutations": grp["Subtype"].apply(lambda s: (s == "POINT").sum()),
    "n_disrupt": grp["Subtype"].apply(lambda s: (s == "POINT_DISRUPT").sum()),
})
stress = tout[tout["Type"] == "STRESS"].groupby("accession").size().rename("n_stress")

resume = meta.set_index("accession")[["categorie"]].join(resume).join(stress)
colonnes = ["n_amr", "n_classes", "n_acquis", "n_mutations", "n_disrupt", "n_stress"]
resume[colonnes] = resume[colonnes].fillna(0).astype(int)
resume = resume.sort_values(["categorie", "n_amr"])
resume.to_csv(f"{R}/panel30_resume_par_genome.tsv", sep="\t")

print("Contrôle :", int(resume["n_amr"].sum() + resume["n_stress"].sum()), "lignes (attendu : 378)")
print()
print(resume.to_string())
print()
print(resume.groupby("categorie")["n_amr"].describe()[["count", "min", "50%", "max"]])
