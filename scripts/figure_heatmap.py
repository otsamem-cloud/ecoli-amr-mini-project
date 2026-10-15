import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

R = "/mnt/c/Bioinfo_RAM/Results"
souches = ["K-12 MG1655", "SE11", "UTI89", "SMS-3-5", "ETEC H10407"]

tout = pd.read_csv(f"{R}/panel_amr_combine.tsv", sep="\t")
presence = (pd.crosstab(tout["Class"], tout["Souche"]) > 0).astype(int)
presence = presence.reindex(columns=souches, fill_value=0)

n_lignes, n_cols = presence.shape
cmap = plt.get_cmap("Blues")

fig, ax = plt.subplots(figsize=(8, 5))
ax.imshow(presence.values, cmap=cmap, vmin=0, vmax=1, aspect="auto")

# étiquettes au centre des cases
ax.set_xticks(range(n_cols))
ax.set_xticklabels(presence.columns, rotation=45, ha="right")
ax.set_yticks(range(n_lignes))
ax.set_yticklabels(presence.index)

# quadrillage blanc entre les cases (aux bords des cases : -0.5, 0.5, 1.5...)
ax.set_xticks([i - 0.5 for i in range(n_cols + 1)], minor=True)
ax.set_yticks([i - 0.5 for i in range(n_lignes + 1)], minor=True)
ax.grid(which="minor", color="white", linewidth=2)
ax.tick_params(which="minor", length=0)

ax.set_title("Classes d'antibiotiques détectées\nAMRFinderPlus 4.2.7, base 2026-08-07.1")

# légende
legende = [
    Patch(facecolor=cmap(1.0), label="Détectée"),
    Patch(facecolor=cmap(0.0), edgecolor="grey", label="Non détectée"),
]
ax.legend(handles=legende, loc="upper left", bbox_to_anchor=(1.02, 1))

fig.savefig(f"{R}/panel_amr_heatmap.png", dpi=200, bbox_inches="tight")
print("Figure enregistrée :", f"{R}/panel_amr_heatmap.png")
