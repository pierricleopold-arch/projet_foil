### ==========================================
### EXTRACTION DES RESULTATS BEAMDYN
### ET EXPORT AU FORMAT TECPLOT
### ==========================================

import pandas as pd

# ------------------------------------------
# 1. Lecture du fichier BeamDyn
# ------------------------------------------

fichier = "data/Dvr_5MW_Dynamic.out"

with open(fichier, "r") as f:
    lignes = f.readlines()


# ------------------------------------------
# 2. Recherche de la ligne d'en-tête
# ------------------------------------------

n = None

for i in range(len(lignes)):
    if lignes[i].strip().startswith("Time"):
        n = i
        break

if n is None:
    raise ValueError("Impossible de trouver l'en-tête Time dans le fichier BeamDyn.")


# ------------------------------------------
# 3. Extraction des données numériques
# ------------------------------------------

df = pd.read_csv(
    fichier,
    sep=r"\s+",
    skiprows=n
).iloc[1:].astype(float)

# Réinitialisation des indices
df = df.reset_index(drop=True)

print("Lecture du fichier BeamDyn terminée.")
print("Nombre de lignes :", len(df))
print("Nombre de variables :", len(df.columns))


# ------------------------------------------
# 4. Sélection des variables à exporter
# ------------------------------------------

variables = [
    "Time",

    # Forces de réaction à l'encastrement
    "RootFxr", "RootFyr", "RootFzr",

    # Moments de réaction à l'encastrement
    "RootMxr", "RootMyr", "RootMzr",

    # Forces au nœud 1
    "N1Fxl", "N1Fyl", "N1Fzl",

    # Moments au nœud 1
    "N1Mxl", "N1Myl", "N1Mzl",

    # Déplacements en bout de poutre
    "TipTDxr", "TipTDyr", "TipTDzr",

    # Rotations en bout de poutre (paramètres de Wiener-Milenkovic)
    "TipRDxr", "TipRDyr", "TipRDzr"
]


# ------------------------------------------
# 5. Vérification des variables disponibles
# ------------------------------------------

variables_valides = [
    v for v in variables if v in df.columns
]

variables_absentes = [
    v for v in variables if v not in df.columns
]

if variables_absentes:
    print("Attention : variables absentes :", variables_absentes)

if "Time" not in variables_valides:
    raise ValueError("La variable Time est absente des résultats.")

# Élimination des éventuels doublons en conservant l'ordre
variables_valides = list(dict.fromkeys(variables_valides))

df_export = df[variables_valides]


# ------------------------------------------
# 6. Export au format Tecplot ASCII
# ------------------------------------------

fichier_sortie = "BeamDyn_Results.dat"

with open(fichier_sortie, "w", newline="") as f:

    # Titre du fichier
    f.write('TITLE = "BeamDyn Results"\n')

    # Noms des variables
    f.write(
        "VARIABLES = "
        + ", ".join(f'"{v}"' for v in variables_valides)
        + "\n"
    )

    # Définition de la zone de données
    f.write(
        f'ZONE T="BeamDyn", I={len(df_export)}, DATAPACKING=POINT\n'
    )

    # Écriture des valeurs numériques
    df_export.to_csv(
        f,
        sep=" ",
        index=False,
        header=False,
        float_format="%.8e",
        lineterminator="\n"
    )


# ------------------------------------------
# 7. Confirmation de l'export
# ------------------------------------------

print("\nExport Tecplot terminé !")
print("Fichier créé :", fichier_sortie)
print("Nombre de variables exportées :", len(variables_valides))
print("Nombre de points exportés :", len(df_export))