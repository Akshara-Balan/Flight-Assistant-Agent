# tools.py
def get_weather(location):
    # Simulated weather data (replace with a real API later if desired)
    weather_data = {
        "Paris": "Sunny, 20°C",
        "Tokyo": "Rainy, 15°C",
        "New York": "Cloudy, 18°C"
    }
    return weather_data.get(location, "Clear, 22°C")  # Default if location not found