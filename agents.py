# agents.py
from data import flights, bookings
from tools import lookup_flights, get_mock_weather, is_flight_delayed

class PreferenceAgent:
    def gather_preferences(self):
        """Gather user preferences via CLI."""
        departure = input("Departure city (optional, press Enter to skip): ").strip() or None
        destination = input("Destination city: ")
        time_pref = input("Preferred time of day (e.g., morning, afternoon): ").lower()
        seat_pref = input("Preferred seat type (economy/business): ").lower()
        return {"departure": departure, "destination": destination, "time": time_pref, "seat": seat_pref}

class FlightLookupAgent:
    def search_flights(self, preferences):
        """Search for flights based on preferences."""
        available_flights = lookup_flights(preferences["destination"], preferences["departure"])
        filtered_flights = []
        
        for flight in available_flights:
            time_match = True
            if preferences["time"] == "morning" and not flight["time"].startswith("0"):
                time_match = False
            elif preferences["time"] == "afternoon" and flight["time"].startswith("0"):
                time_match = False
            
            seat_match = flight["seats"].get(preferences["seat"], 0) > 0
            
            if time_match and seat_match:
                filtered_flights.append(flight)
        
        return filtered_flights

class FlightBookingAgent:
    def book_flight(self, flight_id, user_id, seat_type):
        """Book a flight for a user."""
        flight = next((f for f in flights if f["id"] == flight_id), None)
        if not flight:
            return "Flight not found."
        
        if flight["seats"].get(seat_type, 0) <= 0:
            return "No seats available in that class."
        
        booking_id = len(bookings) + 1
        bookings[booking_id] = {
            "user_id": user_id,
            "flight_id": flight_id,
            "seat_type": seat_type
        }
        flight["seats"][seat_type] -= 1
        return f"Booking confirmed! Booking ID: {booking_id}"

class FlightCancellationAgent:
    def cancel_booking(self, booking_id):
        """Cancel a booking and free up the seat."""
        if booking_id not in bookings:
            return "Booking not found."
        
        booking = bookings[booking_id]
        flight = next((f for f in flights if f["id"] == booking["flight_id"]), None)
        if flight:
            flight["seats"][booking["seat_type"]] += 1
        
        del bookings[booking_id]
        return "Booking cancelled successfully."

class FlightMonitoringAgent:
    def monitor_flight(self, booking_id):
        """Monitor flight status and weather."""
        if booking_id not in bookings:
            return "Booking not found."
        
        booking = bookings[booking_id]
        flight = next((f for f in flights if f["id"] == booking["flight_id"]), None)
        if not flight:
            return "Flight data unavailable."
        
        status = "Delayed" if is_flight_delayed(flight["price"]) else "On Time"
        weather = get_mock_weather(flight["destination"])
        return f"Flight from {flight['departure']} to {flight['destination']} at {flight['time']} " \
               f"(Duration: {flight['duration']}) - Status: {status}, Weather: {weather}"

class OrchestratorAgent:
    def __init__(self):
        self.pref_agent = PreferenceAgent()
        self.lookup_agent = FlightLookupAgent()
        self.booking_agent = FlightBookingAgent()
        self.cancel_agent = FlightCancellationAgent()
        self.monitor_agent = FlightMonitoringAgent()

    def run(self):
        user_id = "user123"  # Hardcoded for simplicity
        while True:
            print("\n=== Travel Assistant ===")
            print("1. Search Flights")
            print("2. Book Flight")
            print("3. Cancel Booking")
            print("4. Monitor Flight")
            print("5. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                prefs = self.pref_agent.gather_preferences()
                flights_found = self.lookup_agent.search_flights(prefs)
                if flights_found:
                    for f in flights_found:
                        print(f"ID: {f['id']}, {f['airline']} from {f['departure']} to {f['destination']}, "
                              f"Time: {f['time']}, Duration: {f['duration']}, Price: ${f['price']}, Seats: {f['seats']}")
                else:
                    print("No flights found matching your preferences.")

            elif choice == "2":
                flight_id = int(input("Enter flight ID to book: "))
                seat_type = input("Enter seat type (economy/business): ").lower()
                result = self.booking_agent.book_flight(flight_id, user_id, seat_type)
                print(result)

            elif choice == "3":
                booking_id = int(input("Enter booking ID to cancel: "))
                result = self.cancel_agent.cancel_booking(booking_id)
                print(result)

            elif choice == "4":
                booking_id = int(input("Enter booking ID to monitor: "))
                result = self.monitor_agent.monitor_flight(booking_id)
                print(result)

            elif choice == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Try again.")