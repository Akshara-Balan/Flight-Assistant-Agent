# agents.py
import ollama
from tools import get_weather  # Assuming this is in a separate file named tools.py

class DestinationAgent:
    def research(self, location):
        prompt = f"Provide a brief overview of {location} for a traveler, including 3 key attractions."
        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]

class ActivityAgent:
    def plan_activities(self, location, days, preferences, destination_info):
        prompt = (
            f"Based on this info about {location}: '{destination_info}', "
            f"plan a {days}-day itinerary for someone who likes {preferences}. "
            f"List one activity per day."
        )
        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]

class OrchestratorAgent:
    def __init__(self):
        self.destination_agent = DestinationAgent()
        self.activity_agent = ActivityAgent()

    def generate_itinerary(self, location, days, preferences):
        # Step 1: Get destination info
        destination_info = self.destination_agent.research(location)
        
        # Step 2: Get weather (tool use)
        weather = get_weather(location)
        
        # Step 3: Plan activities
        activities = self.activity_agent.plan_activities(location, days, preferences, destination_info)
        
        # Step 4: Compile itinerary
        itinerary = (
            f"Travel Itinerary for {location}\n"
            f"Duration: {days} days\n"
            f"Weather: {weather}\n"
            f"Destination Overview:\n{destination_info}\n\n"
            f"Daily Activities:\n{activities}"
        )
        return itinerary