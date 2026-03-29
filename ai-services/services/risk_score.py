from datetime import date
from models.segment import Segment, RoadType
from services.weather import get_weather_score   # ← importer

def normalize_age(construction_year: int) -> float:
    age = 2025 - construction_year
    return min((age / 30) * 100, 100)

def normalize_maintenance(last_maintenance_date: date) -> float:
    days = (date.today() - last_maintenance_date).days
    return min((days / 1095) * 100, 100)

def normalize_traffic(road_type: RoadType) -> float:
    mapping = {
        RoadType.AUTOROUTE: 100,
        RoadType.NATIONALE: 75,
        RoadType.URBAINE:   60,
        RoadType.REGIONALE: 45
    }
    return mapping.get(road_type, 50)

def get_mock_reports_score() -> float:
    return 50  # simulé — remplacer quand API reports prête

def get_status(score: float) -> str:
    if score >= 80:
        return "Critique"
    elif score >= 40:
        return "Dégradé"
    else:
        return "Bon"

def calculate_risk_score(segment: Segment) -> dict:
    age_score         = normalize_age(segment.construction_year)
    maintenance_score = normalize_maintenance(segment.last_maintenance_date)
    traffic_score     = normalize_traffic(segment.road_type)
    reports_score     = get_mock_reports_score()
    weather_score     = get_weather_score(        # ← vraie API météo
                            segment.geometry.lat,
                            segment.geometry.lon
                        )

    risk_score = round(
        age_score         * 0.30 +
        maintenance_score * 0.25 +
        traffic_score     * 0.20 +
        reports_score     * 0.15 +
        weather_score     * 0.10,
        2
    )

    return {
        "risk_score": risk_score,
        "status": get_status(risk_score),
        "detail": {
            "age_score":         round(age_score, 2),
            "maintenance_score": round(maintenance_score, 2),
            "traffic_score":     round(traffic_score, 2),
            "reports_score":     round(reports_score, 2),
            "weather_score":     round(weather_score, 2)
        }
    }
