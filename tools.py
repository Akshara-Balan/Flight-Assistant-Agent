# tools.py
import sqlite3
import requests
import uuid

def get_db_connection():
    return sqlite3.connect("travel.db")

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
                    "legs": None,
                    "status": flight["flight_status"],
                    "source": "AviationStack"
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

def lookup_db_flights(departure, destination):
    """Fetch flights from SQLite."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM flights WHERE departure = ? AND destination = ?", (departure, destination))
    direct_flights = c.fetchall()
    conn.close()
    flights = [dict(zip([desc[0] for desc in c.description], row)) for row in direct_flights]
    for flight in flights:
        flight["source"] = "SQLite"
    print(f"SQLite: {len(flights)} flights from {departure} to {destination}")
    return flights

def find_connecting_flights(departure, destination):
    """Find connecting flights in SQLite."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT f1.*, f2.*
        FROM flights f1
        JOIN flights f2 ON f1.destination = f2.departure
        WHERE f1.departure = ? AND f2.destination = ?
    """, (departure, destination))
    connecting = c.fetchall()
    conn.close()
    print(f"SQLite: {len(connecting)//2} connecting flights from {departure} to {destination}")
    return connecting

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
        
        # Simple delay check: extreme weather conditions
        delay_risk = "Possible delay" if any([
            "rain" in condition, "storm" in condition, "snow" in condition,
            temp_c < -10 or temp_c > 40, wind_kph > 50
        ]) else "No delay expected"
        
        return f"{condition.capitalize()}, {temp_c}°C, Wind: {wind_kph} kph - {delay_risk}"
    except (requests.RequestException, KeyError):
        return "Weather data unavailable"

def generate_ticket_id():
    """Generate a unique ticket ID."""
    return str(uuid.uuid4())[:8].upper()