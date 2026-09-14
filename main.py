import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

city = "Chicago,US"  # You can change this to any city you want to check
url = "https://api.openweathermap.org/data/2.5/forecast"
params = {
    "q": city,
    "appid": api_key,
    "units": "imperial"
}

response = requests.get(url, params=params)
data = response.json()

# Pull out the next forecast entry (roughly the next 3 hours)
next_forecast = data["list"][0]

wind_speed = next_forecast["wind"]["speed"]
precipitation_chance = next_forecast.get("pop", 0) * 100  # "pop" = probability of precipitation, 0-1
conditions = next_forecast["weather"][0]["description"]
visibility = next_forecast.get("visibility", 10000)  # meters, defaults to 10km if missing

print(f"City: {city}")
print(f"Conditions: {conditions}")
print(f"Wind speed: {wind_speed} mph")
print(f"Precipitation chance: {precipitation_chance}%")
print(f"Visibility: {visibility} meters")

def assess_travel_disruption(wind_speed, precipitation_chance, visibility):
    disruption_score = 0

    # Wind contribution
    if wind_speed > 25:
        disruption_score += 2
    elif wind_speed >= 15:
        disruption_score += 1

    # Precipitation contribution
    if precipitation_chance > 60:
        disruption_score += 2
    elif precipitation_chance >= 30:
        disruption_score += 1

    # Visibility contribution
    if visibility < 3000:
        disruption_score += 2
    elif visibility <= 6000:
        disruption_score += 1

    # Convert score to a rating
    if disruption_score >= 4:
        return "High"
    elif disruption_score >= 2:
        return "Moderate"
    else:
        return "Low"

travel_disruption_rating = assess_travel_disruption(wind_speed, precipitation_chance, visibility)
print(f"Travel Disruption Rating: {travel_disruption_rating}")