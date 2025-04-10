# agents.py
from tools import get_db_connection, lookup_flights, lookup_db_flights, find_connecting_flights, get_weather, generate_ticket_id

class PreferenceAgent:
    def gather_preferences(self, departures, destinations):
        return {"departure": departures, "destination": destinations}

class FlightLookupAgent:
    def search_flights(self, preferences, flight_api_key):
        api_flights = lookup_flights(preferences["departure"], preferences["destination"], flight_api_key)
        db_flights = lookup_db_flights(preferences["departure"], preferences["destination"])
        direct_flights = api_flights + db_flights
        
        connecting = []
        if not direct_flights:
            connecting = find_connecting_flights(preferences["departure"], preferences["destination"])
        
        return {"direct": direct_flights, "connecting": connecting}

class FlightBookingAgent:
    def book_flight(self, flight, user_id, seat_type, passenger_name, passenger_email, weather_api_key):
        conn = get_db_connection()
        c = conn.cursor()
        weather = get_weather(flight["destination"], weather_api_key)
        ticket_id = generate_ticket_id()
        
        c.execute("INSERT INTO bookings (user_id, flight_id, seat_type, passenger_name, passenger_email, ticket_id) VALUES (?, ?, ?, ?, ?, ?)",
                  (user_id, flight["id"], seat_type, passenger_name, passenger_email, ticket_id))
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
        flights = lookup_flights("", "", flight_api_key) + lookup_db_flights("", "")
        flight = next((f for f in flights if f["id"] == flight_id), None)
        
        if not flight:
            conn.close()
            return "Flight data unavailable."
        
        status = flight.get("status", "Unknown")
        weather = get_weather(flight["destination"], weather_api_key)
        conn.close()
        return f"Flight {flight['airline']} {flight['id']} from {flight['departure']} to {flight['destination']} at {flight['time']} " \
               f"- Status: {status}, Weather & Delay Risk: {weather}, Ticket ID: {booking['ticket_id']}"