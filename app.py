import os
import requests
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from streamlit_searchbox import st_searchbox

load_dotenv()
api_key = st.secrets["OPENWEATHER_API_KEY"]

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
        forecast_list = data["list"]

        # --- Current conditions (first entry) ---
        current = forecast_list[0]
        wind_speed = current["wind"]["speed"]
        conditions = current["weather"][0]["description"]
        visibility = current.get("visibility", 10000)
        precipitation_chance = current.get("pop", 0) * 100

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

        # --- 5-Day Forecast Trend ---
        # The API returns 3-hour entries (40 total, 8 per day).
        # We'll pick one entry per day, close to midday, to represent each day.
        st.subheader("5-Day Outlook")

        daily_entries = {}
        for entry in forecast_list:
            dt = datetime.fromtimestamp(entry["dt"])
            date_key = dt.date()
            hour = dt.hour
            # Prefer the entry closest to noon for each day
            if date_key not in daily_entries or abs(hour - 12) < abs(daily_entries[date_key][0] - 12):
                daily_entries[date_key] = (hour, entry)

        sorted_days = sorted(daily_entries.items())[:5]
        forecast_cols = st.columns(len(sorted_days))

        for i, (date_key, (hour, entry)) in enumerate(sorted_days):
            with forecast_cols[i]:
                dt = datetime.fromtimestamp(entry["dt"])
                day_label = dt.strftime("%a")
                day_conditions = entry["weather"][0]["description"]
                day_wind = entry["wind"]["speed"]
                day_pop = entry.get("pop", 0) * 100
                day_visibility = entry.get("visibility", 10000)

                day_rating = assess_travel_disruption(day_wind, day_pop, day_visibility)

                st.markdown(f"**{day_label}**")
                st.caption(day_conditions.title())
                st.write(f"💨 {day_wind:.0f} mph")
                st.write(f"🌧️ {day_pop:.0f}%")
                if day_rating == "Low":
                    st.success(day_rating)
                elif day_rating == "Moderate":
                    st.warning(day_rating)
                else:
                    st.error(day_rating)
    else:
        st.error("Could not fetch weather data. Check the city name and try again.")