# tools.py
def get_weather(location):
    weather_data = {"Paris": "Sunny, 20°C", "Tokyo": "Rainy, 15°C", "New York": "Cloudy, 18°C"}
    return weather_data.get(location, "Clear, 22°C")