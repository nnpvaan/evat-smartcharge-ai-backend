def recommend_charger(
    distance_km: float, availability: int, congestion: float
) -> dict:
    """
    Recommend an EV charger based on distance, availability, and congestion.

    Higher availability improves the score.
    Longer distance and higher congestion reduce the score.
    """

    if distance_km < 0:
        raise ValueError("Distance cannot be negative")

    if availability < 0:
        raise ValueError("Availability cannot be negative")

    if congestion < 0 or congestion > 1:
        raise ValueError("Congestion must be between 0 and 1")

    score = (availability * 10) - (distance_km * 1.5) - (congestion * 20)

    if score >= 20:
        recommendation = "Highly recommended"
    elif score >= 10:
        recommendation = "Recommended"
    else:
        recommendation = "Not recommended"

    return {
        "distance_km": distance_km,
        "availability": availability,
        "congestion": congestion,
        "score": round(score, 2),
        "recommendation": recommendation
    }


def predict_congestion(current_usage: int, charger_capacity: int) -> dict:
    """
    Predict congestion level based on charger usage and capacity.
    """

    if current_usage < 0:
        raise ValueError("Current usage cannot be negative")

    if charger_capacity <= 0:
        raise ValueError("Charger capacity must be greater than zero")

    congestion_rate = current_usage / charger_capacity

    if congestion_rate >= 0.8:
        level = "High"
    elif congestion_rate >= 0.5:
        level = "Medium"
    else:
        level = "Low"

    return {
        "current_usage": current_usage,
        "charger_capacity": charger_capacity,
        "congestion_rate": round(congestion_rate, 2),
        "congestion_level": level
    }


def get_available_chargers() -> list:
    """
    Return sample EV charger data.
    """

    return [
        {
            "id": 1,
            "name": "Melbourne Central EV Charger",
            "location": "Melbourne CBD",
            "available_ports": 4,
            "charger_type": "Fast Charger"
        },
        {
            "id": 2,
            "name": "Docklands EV Station",
            "location": "Docklands",
            "available_ports": 2,
            "charger_type": "Standard Charger"
        },
        {
            "id": 3,
            "name": "Southbank EV Hub",
            "location": "Southbank",
            "available_ports": 6,
            "charger_type": "Ultra-fast Charger"
        }
    ]
