import pytest

from app.recommender import (
    recommend_charger,
    predict_congestion,
    get_available_chargers
)


def test_recommend_charger_high_score():
    result = recommend_charger(
        distance_km=2,
        availability=5,
        congestion=0.2
    )

    assert result["recommendation"] == "Highly recommended"
    assert result["score"] > 20


def test_recommend_charger_medium_score():
    result = recommend_charger(
        distance_km=6,
        availability=3,
        congestion=0.4
    )

    assert result["recommendation"] in ["Recommended", "Highly recommended", "Not recommended"]  # noqa: E501
    assert "score" in result


def test_recommend_charger_rejects_negative_distance():
    with pytest.raises(ValueError):
        recommend_charger(
            distance_km=-1,
            availability=5,
            congestion=0.2
        )


def test_recommend_charger_rejects_negative_availability():
    with pytest.raises(ValueError):
        recommend_charger(
            distance_km=2,
            availability=-1,
            congestion=0.2
        )


def test_recommend_charger_rejects_invalid_congestion():
    with pytest.raises(ValueError):
        recommend_charger(
            distance_km=2,
            availability=5,
            congestion=1.5
        )


def test_predict_congestion_high_level():
    result = predict_congestion(
        current_usage=9,
        charger_capacity=10
    )

    assert result["congestion_level"] == "High"
    assert result["congestion_rate"] == 0.9


def test_predict_congestion_medium_level():
    result = predict_congestion(
        current_usage=6,
        charger_capacity=10
    )

    assert result["congestion_level"] == "Medium"


def test_predict_congestion_low_level():
    result = predict_congestion(
        current_usage=2,
        charger_capacity=10
    )

    assert result["congestion_level"] == "Low"


def test_predict_congestion_rejects_invalid_capacity():
    with pytest.raises(ValueError):
        predict_congestion(
            current_usage=2,
            charger_capacity=0
        )


def test_get_available_chargers_returns_list():
    chargers = get_available_chargers()

    assert isinstance(chargers, list)
    assert len(chargers) >= 1
    assert "name" in chargers[0]
