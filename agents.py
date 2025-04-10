# agents.py
from tools import get_db_connection, lookup_flights, get_weather, generate_ticket_id

class PreferenceAgent:
    def gather_preferences(self, departures, destinations):
        return {"departure": departures, "destination": destinations}

class FlightLookupAgent:
    def search_flights(self, preferences, flight_api_key):
        flights = lookup_flights(preferences["departure"], preferences["destination"], flight_api_key)
        return {"direct": flights, "connecting": []}

class FlightBookingAgent:
    def book_flight(self, flight, user_id, seat_type, passenger_name, passenger_email, weather_api_key):
        conn = get_db_connection()
        c = conn.cursor()
        weather = get_weather(flight["destination"], weather_api_key)
        ticket_id = generate_ticket_id()
        
        # Store departure and destination along with other details
        c.execute("INSERT INTO bookings (user_id, flight_id, seat_type, passenger_name, passenger_email, ticket_id, departure, destination) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (user_id, flight["id"], seat_type, passenger_name, passenger_email, ticket_id, flight["departure"], flight["destination"]))
        booking_id = c.lastrowid
        conn.commit()
        conn.close()
        return f"Booking confirmed! Booking ID: {booking_id}, Ticket ID: {ticket_id}, " \
               f"Flight: {flight['airline']} {flight['id']} from {flight['departure']} to {flight['destination']} at {flight['time']}, " \
               f"Passenger: {passenger_name}, Email: {passenger_email}, Destination Weather: {weather}"

class FlightCancellationAgent:
    def cancel_booking(self, booking_id):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
        booking = c.fetchone()
        if not booking:
            conn.close()
            return "Booking not found."
        
        c.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        conn.commit()
        conn.close()
        return "Booking cancelled successfully."

class FlightMonitoringAgent:
    def monitor_flight(self, booking_id, flight_api_key, weather_api_key):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
        booking = c.fetchone()
        if not booking:
            conn.close()
            return "Booking not found."
        
        booking = dict(zip([desc[0] for desc in c.description], booking))
        flight_id = booking["flight_id"]
        departure = booking["departure"]
        destination = booking["destination"]
        
        # Fetch flights for this specific route
        flights = lookup_flights(departure, destination, flight_api_key)
        flight = next((f for f in flights if f["id"] == flight_id), None)
        
        if not flight:
            # Fallback: Use stored booking data if API doesn't return the flight
            weather = get_weather(destination, weather_api_key)
            conn.close()
            return f"Flight {flight_id} from {departure} to {destination} (real-time data unavailable) " \
                   f"- Status: Unknown, Weather & Delay Risk: {weather}, Ticket ID: {booking['ticket_id']}"
        
        status = flight.get("status", "Unknown")
        weather = get_weather(flight["destination"], weather_api_key)
        conn.close()
        return f"Flight {flight['airline']} {flight['id']} from {flight['departure']} to {flight['destination']} at {flight['time']} " \
               f"- Status: {status}, Weather & Delay Risk: {weather}, Ticket ID: {booking['ticket_id']}"