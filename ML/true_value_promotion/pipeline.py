"""
PIPELINE — INGESTION → CLEANING
--------------------------------

This file connects the ingestion and cleaning modules.

It replaces the first part of Sharon’s notebook:
1. Load Coles, Woolworths, IGA CSVs
2. Inspect raw data
3. Clean the datasets

After this step is verified, we will extend the pipeline to:
- harmonisation
- feature engineering
- scoring
- output formatting
"""

# from ingestion import load_retailer_data
from .ingestion import load_all_retailers, load_coles, load_iga, load_woolworths
from .cleaning import clean_all


def run_ingestion_and_cleaning():
    """
    Step 1 of the refactored TVP pipeline:
    - Load raw retailer datasets
    - Clean them using the cleaning module

    This corresponds to the notebook sections:
    "Data Loading and Initial Inspection"
    and
    "Cleaning"
    """

    # -----------------------------
    # Load raw retailer data
    # -----------------------------
    # These functions come from ingestion.py
    print("Loading retailer datasets...")

    coles_df = load_coles()
    wool_df = load_woolworths()
    iga_df = load_iga()

    print("Raw data loaded successfully.\n")


    # -----------------------------
    # Clean each dataset
    # -----------------------------
    # This applies the cleaning steps from cleaning.py
    print("Cleaning Coles data...")
    coles_clean = clean_all(coles_df, "coles")

    print("Cleaning Woolworths data...")
    wool_clean = clean_all(wool_df, "woolworths")

    print("Cleaning IGA data...")
    iga_clean = clean_all(iga_df, "iga")

    print("Cleaning completed.\n")

    
    # -----------------------------
    # Inspect cleaned output
    # -----------------------------
    # This replaces the notebook's "print(df.head())"
    print("Coles cleaned sample:")
    print(coles_clean.head(), "\n")
    print("Coles column names:")
    print(coles_clean.columns.tolist())
    print("Missing values in Coles:", coles_clean.isna().sum().sum())
    print("\nPrice columns sample:")
    print(coles_clean[['price_now', 'price_was']].head())

    print("Woolworths cleaned sample:")
    print(wool_clean.head(), "\n")
    print("Woolworths column names:")
    print(wool_clean.columns.tolist())
    print("Missing values in Woolworths:", wool_clean.isna().sum().sum())
    print("\nPrice columns sample:")
    print(wool_clean[['price_now', 'price_was']].head())

    print("IGA cleaned sample:")
    print(iga_clean.head(), "\n")
    print("IGA column names:")
    print(iga_clean.columns.tolist())
    print("Missing values in IGA:", iga_clean.isna().sum().sum())
    print("\nPrice columns sample:")
    print(iga_clean[['price_now', 'price_was']].head())
    print("\nIGA category sample:")
    print(iga_clean[['category']].head())

    # Return cleaned data for next pipeline steps
    return coles_clean, wool_clean, iga_clean



if __name__ == "__main__":
    # Running this file will execute ingestion → cleaning
    run_ingestion_and_cleaning()
