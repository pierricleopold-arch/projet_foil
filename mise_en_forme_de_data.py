### code python extraction BeamDyn

import pandas as pd
import matplotlib.pyplot as plt

fichier = "data/Dvr_5MW_Dynamic.out"

# Trouver la ligne d'en-tête (celle qui commence par "Time")
with open(fichier) as f:
    lignes = f.readlines()

n = 0
for i in range(len(lignes)):
    if lignes[i].strip().startswith("Time"):
        n = i
        break

df = pd.read_csv(fichier, sep=r"\s+", skiprows=n).iloc[1:].astype(float)
time = df["Time"]


def tracer(base, suffixe, titre, ylabel, unite):
    """Trace les 3 composantes x, y, z d'une grandeur sur un même graphique.
    Exemple : base="RootF", suffixe="r" -> RootFxr, RootFyr, RootFzr"""
    fig, ax = plt.subplots(figsize=(8, 5))
    maxima = []

    for axe, couleur in zip(["x", "y", "z"], ["g", "b", "r"]):
        nom = base + axe + suffixe
        ax.plot(time, df[nom], label=nom, color=couleur)
        maxima.append(f"{nom}: {df[nom].abs().max():.2e} {unite}")

    ax.set_xlabel("Temps (s)")
    ax.set_ylabel(ylabel)
    ax.set_title("ESSAI - " + titre)
    fig.suptitle("Max —> " + " | ".join(maxima), fontsize=10, color="darkred")

    ax.legend(loc="upper left")
    ax.minorticks_on()
    ax.grid(True, which="minor", linestyle=":", linewidth=0.4, color="gray")
    ax.grid(True, which="major", linestyle="--", linewidth=0.5, color="gray")
    plt.tight_layout()


tracer("RootF", "r", "Forces de réaction à l'encastrement (RootF)", "Force (N)", "N")
tracer("RootM", "r", "Moments de réaction à l'encastrement (RootM)", "Moment (N·m)", "N·m")
tracer("N1F", "l", "Forces au nœud 1 (N1F)", "Force (N)", "N")
tracer("N1M", "l", "Moments au nœud 1 (N1M)", "Moment (N·m)", "N·m")
tracer("TipTD", "r", "Déplacements en bout de poutre (TipTD)", "Déplacement (m)", "m")
tracer("TipRD", "r", "Rotations en bout de poutre (TipRD)", "Rotation (param. W-M)", "")

plt.show()