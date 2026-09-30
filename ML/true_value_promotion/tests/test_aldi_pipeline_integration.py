import pandas as pd

from ML.true_value_promotion.aldi_adapter import adapt_aldi_to_tvp
from ML.true_value_promotion.feature_engineering import add_aldi_historical_pricing
from ML.true_value_promotion.aldi_category_mapping import add_aldi_categories
from ML.true_value_promotion.harmonisation import harmonise_aldi
from ML.true_value_promotion.scoring import run_scoring_pipeline
from ML.true_value_promotion.promotion_detection import run_promotion_pipeline


def test_aldi_current_pipeline_integration():
    """
    Verify that Aldi records can pass through the current
    harmonisation, scoring and promotion-detection pipeline.
    """

    aldi_raw = pd.DataFrame({
        "product_id": [
            "aldi-product-1",
            "aldi-product-1",
            "aldi-product-2",
        ],
        "item_name": [
            "Test Aldi Product",
            "Test Aldi Product",
            "Second Aldi Product",
        ],
        "price": [
            5.00,
            4.00,
            3.00,
        ],
        "unit_price": [
            "5.00",
            "4.00",
            "3.00",
        ],
        "is_on_special": [
            False,
            True,
            False,
        ],
        "special_text": [
            None,
            None,
            None,
        ],
        "category_id": [
            "94e9a96c-c9a2-4f7b-a688-c166e6a3cb2b",
            "94e9a96c-c9a2-4f7b-a688-c166e6a3cb2b",
            "94e9a96c-c9a2-4f7b-a688-c166e6a3cb2b",
        ],
        "product_url": [
            "",
            "",
            "",
        ],
        "recorded_at": [
            "2026-08-01 10:00:00",
            "2026-08-02 10:00:00",
            "2026-08-02 10:00:00",
        ],
    })

    adapted = adapt_aldi_to_tvp(aldi_raw)
    features = add_aldi_historical_pricing(adapted)
    features = add_aldi_categories(features)

    harmonised = harmonise_aldi(features)

    assert len(harmonised) == 3
    assert set(harmonised["retailer"]) == {"aldi"}

    required_columns = {
        "retailer",
        "product_id",
        "name",
        "category",
        "price_now",
        "price_was",
        "unit_price",
        "promotiontype",
    }

    assert required_columns.issubset(harmonised.columns)

    # Second observation falls from $5 to $4.
    measurable = harmonised[
        harmonised["price_was"].notna()
        & (harmonised["price_now"] < harmonised["price_was"])
    ]

    assert len(measurable) == 1

    scored = run_scoring_pipeline(harmonised)
    promotions = run_promotion_pipeline(scored)

    assert "tvp_score" in scored.columns
    assert "promotion_valid" in promotions.columns
    assert "promotion_label" in promotions.columns

    valid = promotions[promotions["promotion_valid"]]

    assert len(valid) == 1
    assert valid.iloc[0]["product_id"] == "aldi-product-1"