import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

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

st.title("Travel Disruption Checker")
city = st.text_input("Enter a city (format: City,CountryCode)", "Miami,US")

if st.button("Check Travel Risk"):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": api_key, "units": "imperial"}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        next_forecast = data["list"][0]
        wind_speed = next_forecast["wind"]["speed"]
        precipitation_chance = next_forecast.get("pop", 0) * 100
        conditions = next_forecast["weather"][0]["description"]
        visibility = next_forecast.get("visibility", 10000)
        rating = assess_travel_disruption(wind_speed, precipitation_chance, visibility)

        st.subheader(f"Results for {city}")
        st.write(f"Conditions: {conditions}")
        st.write(f"Wind speed: {wind_speed} mph")
        st.write(f"Precipitation chance: {precipitation_chance}%")
        st.write(f"Visibility: {visibility} meters")
        st.write(f"**Travel Disruption Rating: {rating}**")
    else:
        st.error("Could not fetch weather data. Check the city name and try again.")