import os
import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_searchbox import st_searchbox

load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(page_title="Travel Disruption Checker", page_icon="✈️", layout="centered")

def assess_travel_disruption(wind_speed, precipitation_chance, visibility):
    disruption_score = 0
    if wind_speed > 25:
        disruption_score += 2
    elif wind_speed >= 15:
        disruption_score += 1
    if precipitation_chance > 60:
        disruption_score += 2
    elif precipitation_chance >= 30:
        disruption_score += 1
    if visibility < 3000:
        disruption_score += 2
    elif visibility <= 6000:
        disruption_score += 1
    if disruption_score >= 4:
        return "High"
    elif disruption_score >= 2:
        return "Moderate"
    else:
        return "Low"

def search_locations(searchterm):
    if not searchterm:
        return []
    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": searchterm, "limit": 5, "appid": api_key}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []
    results = response.json()
    options = []
    for r in results:
        label = f"{r['name']}, {r.get('state', '')}, {r['country']}".replace(", , ", ", ")
        options.append((label, r))
    return options

st.title("✈️ Travel Disruption Checker")
st.caption("Check whether weather is likely to disrupt travel to a destination")

selected_city = st_searchbox(
    search_locations,
    placeholder="Start typing a city name...",
    key="city_searchbox",
)

if selected_city:
    lat = selected_city["lat"]
    lon = selected_city["lon"]
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "imperial"}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        next_forecast = data["list"][0]
        wind_speed = next_forecast["wind"]["speed"]
        precipitation_chance = next_forecast.get("pop", 0) * 100
        conditions = next_forecast["weather"][0]["description"]
        visibility = next_forecast.get("visibility", 10000)
        rating = assess_travel_disruption(wind_speed, precipitation_chance, visibility)

        st.subheader(f"Results for {selected_city['name']}")
        st.write(f"Conditions: {conditions.title()}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Wind Speed", f"{wind_speed} mph")
        col2.metric("Precipitation", f"{precipitation_chance:.0f}%")
        col3.metric("Visibility", f"{visibility} m")

        if rating == "Low":
            st.success(f"Travel Disruption Rating: {rating}")
        elif rating == "Moderate":
            st.warning(f"Travel Disruption Rating: {rating}")
        else:
            st.error(f"Travel Disruption Rating: {rating}")
    else:
        st.error("Could not fetch weather data.")