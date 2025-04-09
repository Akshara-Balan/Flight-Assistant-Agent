# agents.py
from transformers import pipeline
from tools import get_weather
class DestinationAgent:
    def research(self, location):
        return (
            f"{location}, a notable destination, offers unique experiences. Key attractions include:\n"
            "1. Famous Landmark\n2. Cultural Site\n3. Scenic Spot"  # Placeholder; replace with my real response
        )

class ActivityAgent:
    def __init__(self):
        self.generator = pipeline("text-generation", model="gpt2", max_length=100)

    def plan_activities(self, location, days, preferences, destination_info):
        prompt = (
            f"Based on: '{destination_info}', plan a {days}-day itinerary for {location} "
            f"for someone who likes {preferences}. List one activity per day."
        )
        result = self.generator(prompt)[0]["generated_text"]
        return result.split(prompt)[-1].strip()

class OrchestratorAgent:
    def __init__(self):
        self.destination_agent = DestinationAgent()
        self.activity_agent = ActivityAgent()

    def generate_itinerary(self, location, days, preferences):
        destination_info = self.destination_agent.research(location)
        weather = get_weather(location)
        activities = self.activity_agent.plan_activities(location, days, preferences, destination_info)
        itinerary = (
            f"Travel Itinerary for {location}\n"
            f"Duration: {days} days\n"
            f"Weather: {weather}\n"
            f"Destination Overview:\n{destination_info}\n\n"
            f"Daily Activities:\n{activities}"
        )
        return itinerary