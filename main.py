# main.py
import streamlit as st
from data import init_db
from agents import PreferenceAgent, FlightLookupAgent, FlightBookingAgent, FlightCancellationAgent, FlightMonitoringAgent
from tools import lookup_db_flights

# Initialize database
init_db()

# Agents
pref_agent = PreferenceAgent()
lookup_agent = FlightLookupAgent()
booking_agent = FlightBookingAgent()
cancel_agent = FlightCancellationAgent()
monitor_agent = FlightMonitoringAgent()

# User ID
user_id = "user123"

# City list
cities = ["Chicago", "New York", "London", "Dubai", "Mumbai", "Delhi", "San Francisco", "Los Angeles",
          "Paris", "Berlin", "Toronto", "Singapore", "Hong Kong", "Seoul", "Moscow", "Beijing",
          "Shanghai", "Rio de Janeiro", "Cape Town", "Sydney", "Tokyo", "Bangalore", "Istanbul"]

# Streamlit UI
st.set_page_config(page_title="Travel Assistant", page_icon="✈️", layout="wide")
st.title("✈️ Travel Assistant")
st.markdown("Plan your journey with ease!")

# Sidebar for API keys
if "flight_api_key" not in st.session_state:
    st.session_state.flight_api_key = ""
if "weather_api_key" not in st.session_state:
    st.session_state.weather_api_key = ""

with st.sidebar:
    st.session_state.flight_api_key = st.text_input("AviationStack API Key", value=st.session_state.flight_api_key, type="password")
    st.session_state.weather_api_key = st.text_input("WeatherAPI.com API Key", value=st.session_state.weather_api_key, type="password")

if not st.session_state.flight_api_key or not st.session_state.weather_api_key:
    st.warning("Please enter both API keys in the sidebar to proceed.")
    st.stop()

option = st.sidebar.selectbox("Choose an action", ["Search Flights", "Book Flight", "Cancel Booking", "Monitor Flight"])

if option == "Search Flights":
    st.subheader("Search Flights")
    col1, col2 = st.columns(2)
    with col1:
        departure = st.selectbox("Departure City", cities)
    with col2:
        destination = st.selectbox("Destination City", cities)
    
    if st.button("Search"):
        prefs = {"departure": departure, "destination": destination}
        result = lookup_agent.search_flights(prefs, st.session_state.flight_api_key)
        
        if result["direct"]:
            st.success("Available Direct Flights:")
            for flight in result["direct"]:
                st.write(f"ID: {flight['id']}, {flight['airline']} from {flight['departure']} to {flight['destination']}, "
                         f"Time: {flight['time']}, Status: {flight.get('status', 'Unknown')}, Source: {flight['source']}")
        elif result["connecting"]:
            st.warning("No direct flights. Connecting flights:")
            for i in range(0, len(result["connecting"]), 2):
                f1 = dict(zip([desc[0] for desc in lookup_db_flights("", "")[0].keys()], result["connecting"][i]))
                f2 = dict(zip([desc[0] for desc in lookup_db_flights("", "")[0].keys()], result["connecting"][i+1]))
                st.write(f"Leg 1: {f1['airline']} from {f1['departure']} to {f1['destination']} at {f1['time']}")
                st.write(f"Leg 2: {f2['airline']} from {f2['departure']} to {f2['destination']} at {f2['time']}")
        else:
            st.error("No flights found from either AviationStack or database.")

elif option == "Book Flight":
    st.subheader("Book a Flight")
    col1, col2 = st.columns(2)
    with col1:
        departure = st.selectbox("Departure City", cities, key="book_dep")
    with col2:
        destination = st.selectbox("Destination City", cities, key="book_dest")
    
    seat_type = st.selectbox("Seat Type", ["Economy", "Business"], key="book_seat")
    
    if st.button("Show Available Flights"):
        prefs = {"departure": departure, "destination": destination}
        flights = lookup_agent.search_flights(prefs, st.session_state.flight_api_key)
        all_flights = flights["direct"]
        
        if "selected_flight" not in st.session_state:
            st.session_state.selected_flight = None
        
        if all_flights:
            st.success("Available Flights:")
            flight_options = {f"{f['airline']} {f['id']} from {f['departure']} to {f['destination']} at {f['time']} (Status: {f.get('status', 'Unknown')}, Source: {f['source']})": f for f in all_flights}
            selected_flight_key = st.selectbox("Select a Flight", list(flight_options.keys()))
            
            if st.button("Proceed to Booking"):
                st.session_state.selected_flight = flight_options[selected_flight_key]
                st.write(f"You’ve selected: {selected_flight_key}")
            
            # Show passenger details form only after proceeding
            if st.session_state.selected_flight:
                st.subheader("Enter Your Details")
                passenger_name = st.text_input("Full Name")
                passenger_email = st.text_input("Email")
                
                if st.button("Confirm Booking") and passenger_name and passenger_email:
                    flight = st.session_state.selected_flight
                    result = booking_agent.book_flight(flight, user_id, seat_type.lower(), passenger_name, passenger_email, st.session_state.weather_api_key)
                    st.write(result)
                    st.session_state.selected_flight = None  # Reset after booking
                elif not passenger_name or not passenger_email:
                    st.warning("Please enter your name and email to confirm booking.")
        elif flights["connecting"]:
            st.warning("No direct flights available. Connecting flights exist:")
            for i in range(0, len(flights["connecting"]), 2):
                f1 = dict(zip([desc[0] for desc in lookup_db_flights("", "")[0].keys()], flights["connecting"][i]))
                f2 = dict(zip([desc[0] for desc in lookup_db_flights("", "")[0].keys()], flights["connecting"][i+1]))
                st.write(f"Leg 1: {f1['airline']} from {f1['departure']} to {f1['destination']} at {f1['time']}")
                st.write(f"Leg 2: {f2['airline']} from {f2['departure']} to {f2['destination']} at {f2['time']}")
            st.info("Connecting flights cannot be booked directly yet.")
        else:
            st.error("No flights available. Check API key or city pair.")

elif option == "Cancel Booking":
    st.subheader("Cancel a Booking")
    booking_id = st.number_input("Booking ID", min_value=1, step=1)
    
    if st.button("Cancel"):
        result = cancel_agent.cancel_booking(booking_id)
        st.write(result)

elif option == "Monitor Flight":
    st.subheader("Monitor a Flight")
    booking_id = st.number_input("Booking ID", min_value=1, step=1)
    
    if st.button("Monitor"):
        result = monitor_agent.monitor_flight(booking_id, st.session_state.flight_api_key, st.session_state.weather_api_key)
        st.write(result)

st.sidebar.markdown("---")
st.sidebar.info("Built with ❤️ by xAI")