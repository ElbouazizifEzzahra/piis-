import httpx

import httpx
from datetime import date, timedelta

def get_weather_score(lat: float, lon: float) -> float:
    # Dates : 30 derniers jours
    end_date   = date.today().strftime("%Y-%m-%d")
    start_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")

    url = (
        f"https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
        f"&daily=precipitation_sum,windspeed_10m_max,temperature_2m_max"
    )

    try:
        response = httpx.get(url, timeout=10)
        data = response.json()
        daily = data["daily"]

        # Moyennes sur 30 jours
        precipitations = daily["precipitation_sum"]
        windspeeds     = daily["windspeed_10m_max"]
        temperatures   = daily["temperature_2m_max"]

        avg_rain = sum(precipitations) / len(precipitations)   # mm/jour moyen
        avg_wind = sum(windspeeds) / len(windspeeds)           # km/h moyen
        max_temp = max(temperatures)                            # température max

        # Calculer le score
        rain_score = min((avg_rain / 10) * 100, 100)   # 10mm/jour = score 100
        wind_score = min((avg_wind / 80) * 100, 100)   # 80km/h = score 100
        temp_score = min((max_temp / 45) * 100, 100)   # 45°C = score 100

        score = (
            rain_score * 0.50 +
            wind_score * 0.30 +
            temp_score * 0.20
        )

        return round(score, 2)

    except Exception:
        return 30  # valeur par défaut raisonnable