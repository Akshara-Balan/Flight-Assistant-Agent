# main.py
from agents import OrchestratorAgent

def main():
    # User input (hardcoded for now, can be made interactive later)
    location = "Paris"
    days = 3
    preferences = "food and culture"

    # Create orchestrator and generate itinerary
    orchestrator = OrchestratorAgent()
    itinerary = orchestrator.generate_itinerary(location, days, preferences)
    
    # Output result
    print(itinerary)

if __name__ == "__main__":
    main()