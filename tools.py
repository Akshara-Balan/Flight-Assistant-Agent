# tools.py
import requests
import uuid
import sqlite3

def lookup_flights(departure, destination, api_key):
    """Fetch real-time flights from AviationStack."""
    try:
        city_to_iata = {
            "Chicago": "ORD", "New York": "JFK", "London": "LHR", "Dubai": "DXB",
            "Mumbai": "BOM", "Delhi": "DEL", "San Francisco": "SFO", "Los Angeles": "LAX",
            "Paris": "CDG", "Berlin": "BER", "Toronto": "YYZ", "Singapore": "SIN",
            "Hong Kong": "HKG", "Seoul": "ICN", "Moscow": "SVO", "Beijing": "PEK",
            "Shanghai": "PVG", "Rio de Janeiro": "GIG", "Cape Town": "CPT", "Sydney": "SYD",
            "Tokyo": "NRT", "Bangalore": "BLR", "Istanbul": "IST"
        }
        dep_iata = city_to_iata.get(departure, departure)
        arr_iata = city_to_iata.get(destination, destination)
        
        url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&dep_iata={dep_iata}&arr_iata={arr_iata}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data["data"]:
            flights = [
                {
                    "id": f"{flight['flight']['iata']}_{flight['flight_date']}",
                    "airline": flight["airline"]["name"],
                    "departure": dep_iata,
                    "destination": arr_iata,
                    "time": flight["departure"]["scheduled"].split("T")[1][:5],
                    "duration": "N/A",
                    "seats_economy": 10 if flight["flight_status"] == "scheduled" else 0,
                    "seats_business": 5 if flight["flight_status"] == "scheduled" else 0,
                    "status": flight["flight_status"]
                }
                for flight in data["data"]
            ]
            print(f"AviationStack: {len(flights)} flights from {dep_iata} to {arr_iata}")
            return flights
        print(f"No AviationStack flights for {dep_iata} to {arr_iata}")
        return []
    except (requests.RequestException, KeyError) as e:
        print(f"AviationStack error: {str(e)}")
        return []

def get_weather(city, api_key):
    """Fetch weather and check for delay conditions."""
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        condition = data["current"]["condition"]["text"].lower()
        temp_c = data["current"]["temp_c"]
        wind_kph = data["current"]["wind_kph"]
        
        delay_risk = "Possible delay" if any([
            "rain" in condition, "storm" in condition, "snow" in condition,
            temp_c < -10 or temp_c > 40, wind_kph > 50
        ]) else "No delay expected"
        
        return f"{condition.capitalize()}, {temp_c}°C, Wind: {wind_kph} kph - {delay_risk}"
    except (requests.RequestException, KeyError):
        return "Weather data unavailable"

def generate_ticket_id():
    return str(uuid.uuid4())[:8].upper()

def get_db_connection():
    return sqlite3.connect("travel.db")