"""
TVP PIPELINE — INGESTION → CLEANING → HARMONISATION → SCORING → PROMOTION DETECTION → FINAL TVP SCORE
--------------------------------------------------------------

This pipeline follows the exact structure of Sharon’s notebook:

1. Ingestion
2. Cleaning
3. Harmonisation
4. Scoring
5. Promotion Detection
6. Final TVP Score

Each stage is modular and testable. This file orchestrates the workflow.
"""

from .ingestion import load_coles, load_woolworths, load_iga
from .cleaning import clean_all
from .harmonisation import harmonise_all
from .scoring import run_scoring_pipeline
from .promotion_detection import run_promotion_pipeline
# from ML.true_value_promotion.final_scoring import compute_final_tvp_score, rank_deals
from ML.true_value_promotion.final_scoring import (
    compute_final_tvp_score,
    rank_deals,
    add_deal_label
)


def run_pipeline():
    """
    Execute the full ingestion → cleaning → harmonisation → scoring → promotion detection workflow.

    This function is the backbone of the refactored TVP system.
    It loads raw retailer data, cleans it, harmonises it into a unified schema,
    applies scoring, runs promotion detection, and returns all intermediate and final outputs.
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
    # STEP 4 — SCORING
    # ---------------------------------------------------------
    print("=== STEP 4: SCORING ===")
    print("Running scoring pipeline...")

    scored_df = run_scoring_pipeline(combined_harmonised)

    print("Scoring completed.\n")
    print("Scored sample:")
    print(scored_df.head(), "\n")

    # ---------------------------------------------------------
    # STEP 5 — PROMOTION DETECTION
    # ---------------------------------------------------------
    print("=== STEP 5: PROMOTION DETECTION ===")
    print("Running promotion detection...")

    promotions_df = run_promotion_pipeline(scored_df)

    print("Promotion detection completed.\n")
    print("Promotion sample:")
    print(promotions_df.head(), "\n")

    # ---------------------------------------------------------
    # STEP 6: FINAL TVP SCORE & DEAL RANKING
    # ---------------------------------------------------------

    df = compute_final_tvp_score(promotions_df)
    df = rank_deals(df)

    print("\n=== STEP 6: FINAL TVP SCORE ===")
    print(df[["retailer", "product_id", "name", "final_tvp_score", "rank"]].head())

    # ---------------------------------------------------------
    # STEP 7: TOP DEALS SELECTION
    # ---------------------------------------------------------
    top_deals = df.head(20)

    print("\n=== STEP 7: TOP DEALS (TOP 20) ===")
    print(top_deals[["retailer", "product_id", "name", "final_tvp_score", "rank"]])

        # ---------------------------------------------------------
    # STEP 8: DEAL LABEL FORMATTING
    # ---------------------------------------------------------
    df = add_deal_label(df)

    print("\n=== STEP 8: DEAL LABELS ===")
    print(df[["retailer", "product_id", "name", "deal_label"]].head())



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
        "scored": scored_df,
        "promotions": promotions_df,
        "final_tvp": df,
        "top_deals": top_deals,
        "deal_labels": df[["product_id", "deal_label"]],


    }


if __name__ == "__main__":
    # Running this file executes the full pipeline
    run_pipeline()
