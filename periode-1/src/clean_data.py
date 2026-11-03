
import json
from pathlib import Path

import pandas as pd

from load_data import load_dataset


# --------------------------------------------------
# 1. CHEMINS DU PROJET
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

OUTPUT_DATA = PROCESSED_DIR / "dataset_clean.csv"
OUTPUT_REPORT = PROCESSED_DIR / "cleaning_report.json"


# --------------------------------------------------
# 2. COLONNES NUMERIQUES ATTENDUES
# --------------------------------------------------

NUMERIC_COLUMNS = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "URLSimilarityIndex",
    "CharContinuationRate",
    "TLDLegitimateProb",
    "URLCharProb",
    "TLDLength",
    "NoOfSubDomain",
    "HasObfuscation",
    "NoOfObfuscatedChar",
    "ObfuscationRatio",
    "NoOfLettersInURL",
    "LetterRatioInURL",
    "NoOfDegitsInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL",
    "IsHTTPS",
    "LineOfCode",
    "LargestLineLength",
    "HasTitle",
    "DomainTitleMatchScore",
    "URLTitleMatchScore",
    "HasFavicon",
    "Robots",
    "IsResponsive",
    "NoOfURLRedirect",
    "NoOfSelfRedirect",
    "HasDescription",
    "NoOfPopup",
    "NoOfiFrame",
    "HasExternalFormSubmit",
    "HasSocialNet",
    "HasSubmitButton",
    "HasHiddenFields",
    "HasPasswordField",
    "Bank",
    "Pay",
    "Crypto",
    "HasCopyrightInfo",
    "NoOfImage",
    "NoOfCSS",
    "NoOfJS",
    "NoOfSelfRef",
    "NoOfEmptyRef",
    "NoOfExternalRef",
    "label",
]


# --------------------------------------------------
# 3. VARIABLES BINAIRES
# --------------------------------------------------

BINARY_COLUMNS = [
    "IsDomainIP",
    "HasObfuscation",
    "IsHTTPS",
    "HasTitle",
    "HasFavicon",
    "Robots",
    "IsResponsive",
    "HasDescription",
    "HasExternalFormSubmit",
    "HasSocialNet",
    "HasSubmitButton",
    "HasHiddenFields",
    "HasPasswordField",
    "Bank",
    "Pay",
    "Crypto",
    "HasCopyrightInfo",
    "NoOfURLRedirect",
    "NoOfSelfRedirect",
]


# --------------------------------------------------
# 4. FONCTION PRINCIPALE DE NETTOYAGE
# --------------------------------------------------

def clean_data():

    # Chargement du dataset original
    df = load_dataset()

    print("\n" + "=" * 60)
    print("DIAGNOSTIC ET PREPARATION DES DONNEES")
    print("=" * 60)

    initial_rows = len(df)
    initial_columns = len(df.columns)

    missing_before = int(df.isna().sum().sum())
    duplicates_before = int(df.duplicated().sum())

    # Vérification des colonnes indispensables
    required_columns = [
        "URL",
        "Domain",
        "Title",
        "HasTitle",
        "URLCharProb",
        "label",
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Colonnes indispensables absentes : {missing_columns}"
        )

    # Vérification de toutes les colonnes numériques attendues
    missing_numeric_columns = [
        col for col in NUMERIC_COLUMNS
        if col not in df.columns
    ]

    if missing_numeric_columns:
        raise ValueError(
            "Colonnes numériques attendues absentes : "
            f"{missing_numeric_columns}"
        )

    print("\nVérification des colonnes numériques : OK")

    # Vérification de la présence des variables binaires
    missing_binary_columns = [
        col for col in BINARY_COLUMNS
        if col not in df.columns
    ]

    if missing_binary_columns:
        raise ValueError(
            "Colonnes binaires attendues absentes : "
            f"{missing_binary_columns}"
        )

    # --------------------------------------------------
    # 5. DIAGNOSTIC DES DOUBLONS
    # --------------------------------------------------

    repeated_url_mask = df["URL"].duplicated(keep=False)

    repeated_url_rows = int(repeated_url_mask.sum())

    repeated_url_occurrences = int(
        df["URL"].duplicated().sum()
    )

    distinct_repeated_urls = int(
        df.loc[repeated_url_mask, "URL"].nunique()
    )

    print(f"\nDimensions initiales : {df.shape}")
    print(f"Valeurs manquantes initiales : {missing_before}")
    print(f"Doublons complets : {duplicates_before}")
    print(f"URL répétées distinctes : {distinct_repeated_urls}")
    print(
        "Lignes concernées par les URL répétées : "
        f"{repeated_url_rows}"
    )

    # --------------------------------------------------
    # 6. VERIFICATION DES LABELS
    # --------------------------------------------------

    labels = pd.to_numeric(df["label"], errors="coerce")

    invalid_labels = (
        labels.isna() | ~labels.isin([0, 1])
    )

    if invalid_labels.any():
        raise ValueError(
            f"{int(invalid_labels.sum())} label(s) invalide(s). "
            "Nettoyage interrompu."
        )

    df["label"] = labels.astype("int64")

    print("\nRépartition des labels :")
    print(df["label"].value_counts().sort_index())

    # --------------------------------------------------
    # 7. COPIE POUR LE NETTOYAGE
    # --------------------------------------------------

    cleaned = df.copy()

    # Nettoyage des espaces dans les colonnes textuelles
    text_columns = [
        "FILENAME",
        "URL",
        "Domain",
        "TLD",
        "Title",
    ]

    for column in text_columns:
        if column in cleaned.columns:
            cleaned[column] = (
                cleaned[column]
                .astype("string")
                .str.strip()
            )

    # --------------------------------------------------
    # 8. CONVERSION DES VARIABLES NUMERIQUES
    # --------------------------------------------------

    invalid_numeric_values = {}

    for column in NUMERIC_COLUMNS:

        original = cleaned[column]

        converted = pd.to_numeric(
            original,
            errors="coerce"
        )

        invalid_mask = (
            original.notna() & converted.isna()
        )

        invalid_count = int(invalid_mask.sum())

        if invalid_count > 0:
            invalid_numeric_values[column] = invalid_count

            # Seule l'anomalie déjà identifiée dans
            # URLCharProb est acceptée automatiquement.
            if column != "URLCharProb":
                raise ValueError(
                    f"Valeurs non numériques inattendues "
                    f"dans {column} : {invalid_count}. "
                    "Vérification nécessaire."
                )

        cleaned[column] = converted

    print("\nConversion des variables numériques : OK")

    # --------------------------------------------------
    # 9. VERIFICATION DES VARIABLES BINAIRES
    # --------------------------------------------------

    invalid_binary_values = {}

    for column in BINARY_COLUMNS:

        invalid_mask = (
            cleaned[column].notna()
            & ~cleaned[column].isin([0, 1])
        )

        invalid_count = int(invalid_mask.sum())

        if invalid_count > 0:
            invalid_values = (
                cleaned.loc[invalid_mask, column]
                .unique()
                .tolist()
            )

            invalid_binary_values[column] = {
                "count": invalid_count,
                "values": invalid_values,
            }

            raise ValueError(
                f"Valeurs invalides dans la variable binaire "
                f"{column} : {invalid_values}. "
                "Seules les valeurs 0 et 1 sont autorisées."
            )

    print(
        f"Vérification des {len(BINARY_COLUMNS)} "
        "variables binaires : OK"
    )

    # --------------------------------------------------
    # 10. TRAITEMENT DU MARQUEUR TITLE = 0
    # --------------------------------------------------

    title_mask = (
        cleaned["HasTitle"].eq(0)
        & cleaned["Title"].eq("0")
    )

    title_markers = int(title_mask.sum())

    cleaned.loc[title_mask, "Title"] = pd.NA

    # --------------------------------------------------
    # 11. VERIFICATIONS FINALES
    # --------------------------------------------------

    if not cleaned["label"].isin([0, 1]).all():
        raise ValueError("Des labels invalides subsistent.")

    final_rows = len(cleaned)
    final_columns = len(cleaned.columns)

    missing_after = int(cleaned.isna().sum().sum())

    # --------------------------------------------------
    # 12. EXPORT DU DATASET PREPARE
    # --------------------------------------------------

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    cleaned.to_csv(
        OUTPUT_DATA,
        index=False
    )

    # --------------------------------------------------
    # 13. CREATION DU RAPPORT
    # --------------------------------------------------

    report = {
        "input_file": "data/raw/dataset.csv",
        "output_file": "data/processed/dataset_clean.csv",

        "initial_rows": initial_rows,
        "final_rows": final_rows,

        "initial_columns": initial_columns,
        "final_columns": final_columns,

        "missing_values_before": missing_before,
        "missing_values_after": missing_after,

        "duplicate_rows": duplicates_before,

        "distinct_repeated_urls": distinct_repeated_urls,
        "rows_with_repeated_urls": repeated_url_rows,
        "repeated_url_occurrences": repeated_url_occurrences,

        "invalid_numeric_values": invalid_numeric_values,

        "binary_columns_checked": BINARY_COLUMNS,
        "binary_values_validated": True,

        "title_absence_markers_replaced": title_markers,

        "rows_removed": initial_rows - final_rows,

        "actions": [
            "Conservation du fichier original",
            "Conservation des lignes et des colonnes",
            "Suppression des espaces superflus dans les colonnes textuelles",
            "Conversion des variables numeriques",
            "Conversion des valeurs invalides de URLCharProb en NaN",
            "Remplacement du marqueur Title = 0 par une valeur manquante lorsque HasTitle = 0",
            "Conservation des URL repetees",
            "Verification des labels 0 et 1",
            "Verification des variables binaires",
            "Verification des colonnes numeriques attendues",
        ],
    }

    with open(
        OUTPUT_REPORT,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    # --------------------------------------------------
    # 14. AFFICHAGE DU BILAN
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("NETTOYAGE TERMINE")
    print("=" * 60)

    print(f"Dimensions finales : {cleaned.shape}")
    print(
        "Valeurs manquantes après nettoyage : "
        f"{missing_after}"
    )
    print(f"Marqueurs Title traités : {title_markers}")
    print(f"Lignes supprimées : {initial_rows - final_rows}")

    print(f"\nDataset préparé : {OUTPUT_DATA}")
    print(f"Rapport : {OUTPUT_REPORT}")


if __name__ == "__main__":
    clean_data()
