# ✈️ Travel Disruption Checker

A web app that pulls live weather forecast data for any city and rates the likelihood of travel disruption due to weather conditions.

**🔗 Live app:** [weather-risk-zlvr4ua7oj7yruthtwzxfz.streamlit.app](https://weather-risk-zlvr4ua7oj7yruthtwzxfz.streamlit.app/)

## What it does

Type a city name into the search bar, select the correct match from live autocomplete suggestions, and the app will:

- Pull current and short-term forecast data from the OpenWeatherMap API
- Calculate a **Travel Disruption Rating** (Low / Moderate / High) based on wind speed, precipitation chance, and visibility
- Display a 5-day outlook showing how disruption risk trends over the coming days

## Why I built this

I built this project to demonstrate practical skills relevant to a Solutions Engineer role: integrating a third-party API, transforming raw data into a business-relevant output, and shipping a working, hosted product rather than just a script. It's designed to reflect how a real customer-facing tool might turn technical data into something a non-technical user can act on quickly.

## How the Travel Disruption Rating works

Each of the three factors below contributes points to an overall disruption score:

| Factor | Low (0 pts) | Moderate (1 pt) | High (2 pts) |
|---|---|---|---|
| Wind speed | < 15 mph | 15–25 mph | > 25 mph |
| Precipitation chance | < 30% | 30–60% | > 60% |
| Visibility | > 6,000m | 3,000–6,000m | < 3,000m |

The combined score maps to a final rating:
- **0–1 points:** Low
- **2–3 points:** Moderate
- **4+ points:** High

## Tech stack

- **Python** — core logic and data processing
- **Streamlit** — front-end web interface
- **OpenWeatherMap API** — live weather and geocoding data
- **streamlit-searchbox** — live autocomplete city search

## Known limitations

- The 5-day outlook uses the free 5-day/3-hour forecast endpoint, which doesn't include visibility data for future days — those days default to treating visibility as clear and rely on wind and precipitation only. This is a documented tradeoff to keep the project on OpenWeatherMap's free tier.
- Weather alerts (e.g., official storm warnings) are not currently included, since that data requires a paid API tier. A free alternative (like the U.S. National Weather Service API) is a planned future addition.

## Running it locally

```bash
git clone https://github.com/yourusername/weather-risk.git
cd weather-risk
pip install -r requirements.txt
```

Create a `.env` file in the project root with:
```
OPENWEATHER_API_KEY=your_api_key_here
```

Then run:
```bash
streamlit run app.py
```

## What's next

- A redesigned front end based on a Figma mockup, focused on improved visual hierarchy and UX
- Possible integration with Microsoft Fabric for enterprise-scale data handling