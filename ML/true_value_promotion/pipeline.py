"""
TVP PIPELINE — INGESTION → CLEANING → HARMONISATION
----------------------------------------------------

This pipeline follows the exact structure of Sharon’s notebook:

1. Ingestion
2. Cleaning
3. Harmonisation
4. (Future) Scoring
5. (Future) Promotion Detection

Each stage is modular and testable. This file orchestrates the workflow.
"""

from .ingestion import load_coles, load_woolworths, load_iga
from .cleaning import clean_all
from .harmonisation import harmonise_all


def run_pipeline():
    """
    Execute the full ingestion → cleaning → harmonisation workflow.

    This function is the backbone of the refactored TVP system.
    It loads raw retailer data, cleans it, harmonises it into a unified schema,
    and returns all intermediate and final outputs for downstream scoring.
    """

    # ---------------------------------------------------------
    # STEP 1 — INGESTION
    # ---------------------------------------------------------
    print("\n=== STEP 1: INGESTION ===")
    print("Loading retailer datasets...")

    coles_raw = load_coles()
    wool_raw = load_woolworths()
    iga_raw = load_iga()

    print("Raw datasets loaded successfully.\n")

    # ---------------------------------------------------------
    # STEP 2 — CLEANING
    # ---------------------------------------------------------
    print("=== STEP 2: CLEANING ===")

    print("Cleaning Coles data...")
    coles_clean = clean_all(coles_raw, "coles")

    print("Cleaning Woolworths data...")
    wool_clean = clean_all(wool_raw, "woolworths")

    print("Cleaning IGA data...")
    iga_clean = clean_all(iga_raw, "iga")

    print("Cleaning completed.\n")

    # Optional: show small samples for debugging
    print("Coles cleaned sample:")
    print(coles_clean.head(), "\n")

    print("Woolworths cleaned sample:")
    print(wool_clean.head(), "\n")

    print("IGA cleaned sample:")
    print(iga_clean.head(), "\n")

    # ---------------------------------------------------------
    # STEP 3 — HARMONISATION
    # ---------------------------------------------------------
    print("=== STEP 3: HARMONISATION ===")
    print("Harmonising retailer datasets...")

    (
        coles_h,
        wool_h,
        iga_h,
        combined_harmonised
    ) = harmonise_all(coles_clean, wool_clean, iga_clean)

    print("Harmonisation completed.\n")

    print("Unified harmonised sample:")
    print(combined_harmonised.head(), "\n")

    # ---------------------------------------------------------
    # RETURN ALL STAGES FOR FUTURE STEPS
    # ---------------------------------------------------------
    return {
        "coles_raw": coles_raw,
        "wool_raw": wool_raw,
        "iga_raw": iga_raw,
        "coles_clean": coles_clean,
        "wool_clean": wool_clean,
        "iga_clean": iga_clean,
        "coles_harmonised": coles_h,
        "wool_harmonised": wool_h,
        "iga_harmonised": iga_h,
        "combined_harmonised": combined_harmonised,
    }


if __name__ == "__main__":
    # Running this file executes the full pipeline
    run_pipeline()
