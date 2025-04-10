# main.py
import streamlit as st
from data import init_db
from agents import PreferenceAgent, FlightLookupAgent, FlightBookingAgent, FlightCancellationAgent, FlightMonitoringAgent

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
st.markdown("Plan your journey with real-time flight data!")

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

# Initialize booking state
if "booking_step" not in st.session_state:
    st.session_state.booking_step = "initial"
if "flights" not in st.session_state:
    st.session_state.flights = []
if "selected_flight" not in st.session_state:
    st.session_state.selected_flight = None

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
                         f"Time: {flight['time']}, Status: {flight['status']}")
        else:
            st.error("No flights found. Check city pair or API status.")

elif option == "Book Flight":
    st.subheader("Book a Flight")
    
    # Step 1: Select cities and seat type
    if st.session_state.booking_step == "initial":
        col1, col2 = st.columns(2)
        with col1:
            departure = st.selectbox("Departure City", cities, key="book_dep")
        with col2:
            destination = st.selectbox("Destination City", cities, key="book_dest")
        
        seat_type = st.selectbox("Seat Type", ["Economy", "Business"], key="book_seat")
        
        if st.button("Find Flights"):
            prefs = {"departure": departure, "destination": destination}
            flights = lookup_agent.search_flights(prefs, st.session_state.flight_api_key)["direct"]
            if flights:
                st.session_state.flights = flights
                st.session_state.seat_type = seat_type
                st.session_state.booking_step = "select_flight"
            else:
                st.error("No flights available for this route today.")
    
    # Step 2: Select flight
    if st.session_state.booking_step == "select_flight" and st.session_state.flights:
        st.success("Available Flights:")
        flight_options = {f"{f['airline']} {f['id']} from {f['departure']} to {f['destination']} at {f['time']} (Status: {f['status']})": f for f in st.session_state.flights}
        selected_flight_key = st.selectbox("Choose Your Flight", list(flight_options.keys()), key="flight_select")
        
        if st.button("Proceed to Book"):
            st.session_state.selected_flight = flight_options[selected_flight_key]
            st.session_state.booking_step = "enter_details"
    
    # Step 3: Enter passenger details
    if st.session_state.booking_step == "enter_details" and st.session_state.selected_flight:
        flight = st.session_state.selected_flight
        st.subheader(f"Booking: {flight['airline']} {flight['id']} at {flight['time']}")
        passenger_name = st.text_input("Full Name", key="name")
        passenger_email = st.text_input("Email", key="email")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirm Booking"):
                if passenger_name and passenger_email:
                    result = booking_agent.book_flight(
                        flight, user_id, st.session_state.seat_type.lower(), passenger_name, passenger_email, st.session_state.weather_api_key
                    )
                    st.write(result)
                    # Reset state
                    st.session_state.booking_step = "initial"
                    st.session_state.flights = []
                    st.session_state.selected_flight = None
                else:
                    st.warning("Please enter your name and email.")
        with col2:
            if st.button("Back to Flights"):
                st.session_state.booking_step = "select_flight"
                st.session_state.selected_flight = None
    
    # Reset option
    if st.session_state.booking_step != "initial":
        if st.button("Start Over"):
            st.session_state.booking_step = "initial"
            st.session_state.flights = []
            st.session_state.selected_flight = None

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