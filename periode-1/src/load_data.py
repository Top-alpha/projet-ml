
from pathlib import Path
import pandas as pd


# Dossier periode-1
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Dataset original
DATA_PATH = PROJECT_DIR / "data" / "raw" / "dataset.csv"


def load_dataset(path: Path = DATA_PATH) -> pd.DataFrame:
    """
    Charge le dataset original URLShield AI.

    Vérifie que le fichier existe et qu'il n'est pas vide.
    Ne modifie jamais le fichier original.
    """

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset introuvable : {path.resolve()}"
        )

    # low_memory=False évite le DtypeWarning lié
    # aux valeurs de types différents dans URLCharProb.
    df = pd.read_csv(path, low_memory=False)

    if df.empty:
        raise ValueError("Le dataset est vide.")

    print(f"Dataset chargé : {path}")
    print(f"Nombre de lignes : {df.shape[0]}")
    print(f"Nombre de colonnes : {df.shape[1]}")

    return df


if __name__ == "__main__":
    dataset = load_dataset()

    print("\nPremières lignes :")
    print(dataset.head())

    print("\nNoms des colonnes :")
    print(dataset.columns.tolist())
