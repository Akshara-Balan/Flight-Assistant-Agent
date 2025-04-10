# Travel Assistant

A Python-based web application built with Streamlit to search, book, cancel, and monitor real-time flights using the AviationStack API and WeatherAPI.com. This tool allows users to plan travel efficiently with a simple interface, storing bookings in SQLite for persistence.

 ## Features

    Search Flights: Find real-time flights between cities using AviationStack.
    
    Book Flights: Select a flight, enter passenger details, and receive a unique ticket ID.
    
    Cancel Bookings: Remove bookings by ID.
    
    Monitor Flights: Check flight status, destination weather, and delay risks.
    
    Real-Time Data: Integrates AviationStack for flights and WeatherAPI.com for weather updates.
    
    Persistent Storage: Saves bookings in an SQLite database.

## Configuration

    API Keys: You’ll need to provide your AviationStack and WeatherAPI.com API keys via the Streamlit sidebar when running the app. No environment variables are required.

## Usage

* Run the Application: Start the Streamlit server:
    bash
```sh
    streamlit run main.py
```
    Opens at http://localhost:8501 in your browser.

* Enter API Keys:

    In the sidebar, input your AviationStack and WeatherAPI.com API keys.

# Features:

    Search Flights: Select departure and destination cities, click "Search" to view available flights.

    Book Flight:
        * Choose cities and seat type (Economy/Business), click "Find Flights".
        * Select a flight from the list, click "Proceed to Book".
        * Enter your name and email, click "Confirm Booking" to save and get a ticket ID.
    
    Cancel Booking: Enter a booking ID, click "Cancel".
    
    Monitor Flight: Enter a booking ID, click "Monitor" to see status and weather.