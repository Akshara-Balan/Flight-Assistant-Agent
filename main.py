# main.py
from agents import OrchestratorAgent

def get_user_input():
    # Prompt for location
    location = input("Enter your travel destination (e.g., Paris, Tokyo, New York): ").strip()
    
    # Prompt for days with validation
    while True:
        try:
            days = int(input("How many days will you stay (e.g., 3): "))
            if days > 0:
                break
            else:
                print("Please enter a positive number of days.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Prompt for preferences
    preferences = input("What do you like (e.g., food, culture, adventure): ").strip()
    
    return location, days, preferences

def main():
    print("Welcome to the Travel Itinerary Generator!")
    # Get user input
    location, days, preferences = get_user_input()
    
    # Create orchestrator and generate itinerary
    orchestrator = OrchestratorAgent()
    itinerary = orchestrator.generate_itinerary(location, days, preferences)
    
    # Output result
    print("\nHere’s your itinerary:\n")
    print(itinerary)

if __name__ == "__main__":
    main()