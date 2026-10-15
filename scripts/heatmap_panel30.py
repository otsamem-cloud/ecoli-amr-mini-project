import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

R = "/mnt/c/Bioinfo_RAM/Results"
tout = pd.read_csv(f"{R}/panel30_amr_combine.tsv", sep="\t")
resume = pd.read_csv(f"{R}/panel30_resume_par_genome.tsv", sep="\t", index_col="accession")

amr = tout[tout["Type"] == "AMR"]
presence = (pd.crosstab(amr["accession"], amr["Class"]) > 0).astype(int)
# les 30 génomes, dans l'ordre du résumé (origine, puis nombre de détections)
presence = presence.reindex(index=resume.index, fill_value=0)
# classes les plus fréquentes à gauche
presence = presence[presence.sum().sort_values(ascending=False).index]

n_lignes, n_cols = presence.shape
cmap = plt.get_cmap("Blues")

fig, ax = plt.subplots(figsize=(12, 9))
ax.imshow(presence.values, cmap=cmap, vmin=0, vmax=1, aspect="auto")

ax.set_xticks(range(n_cols))
ax.set_xticklabels(presence.columns, rotation=60, ha="right")
etiquettes = [f"{resume.loc[a, 'categorie']} | {a}" for a in presence.index]
ax.set_yticks(range(n_lignes))
ax.set_yticklabels(etiquettes, fontsize=8)

# quadrillage blanc entre les cases
ax.set_xticks([i - 0.5 for i in range(n_cols + 1)], minor=True)
ax.set_yticks([i - 0.5 for i in range(n_lignes + 1)], minor=True)
ax.grid(which="minor", color="white", linewidth=1.5)
ax.tick_params(which="minor", length=0)

# trait noir entre deux origines différentes
cats = list(resume.loc[presence.index, "categorie"])
for i in range(1, n_lignes):
    if cats[i] != cats[i - 1]:
        ax.axhline(i - 0.5, color="black", linewidth=1.5)

ax.set_title("Classes d'antibiotiques détectées, par génome et par origine\n"
             "AMRFinderPlus 4.2.7, base 2026-08-07.1 (éléments de type AMR)")
legende = [
    Patch(facecolor=cmap(1.0), label="Détectée"),
    Patch(facecolor=cmap(0.0), edgecolor="grey", label="Non détectée"),
]
ax.legend(handles=legende, loc="upper left", bbox_to_anchor=(1.02, 1))

fig.savefig(f"{R}/panel30_heatmap.png", dpi=200, bbox_inches="tight")
print("Figure enregistrée :", f"{R}/panel30_heatmap.png")
