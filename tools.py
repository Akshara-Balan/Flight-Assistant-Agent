# tools.py
from data import flights

def lookup_flights(destination, departure=None):
    """Return flights matching the destination and optionally departure."""
    if departure:
        return [flight for flight in flights if flight["destination"].lower() == destination.lower() and flight["departure"].lower() == departure.lower()]
    return [flight for flight in flights if flight["destination"].lower() == destination.lower()]

def get_mock_weather(destination):
    """Return mock weather data based on destination."""
    weather_data = {
        "new york": "Sunny, 25°C",
        "london": "Rainy, 15°C",
        "san francisco": "Foggy, 18°C",
        "dubai": "Hot, 35°C"
    }
    return weather_data.get(destination.lower(), "Weather data unavailable")

def is_flight_delayed(price):
    """Simple condition: flights under $200 are delayed."""
    return price < 200