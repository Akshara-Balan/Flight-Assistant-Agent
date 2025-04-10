This project is a console-based AI-powered travel assistant, designed to simulate a user-friendly agent that helps travelers search for flights, book, monitor, and cancel them based on preferences.

🧭 Summary of What the Project Does
💡 Purpose:

To provide an interactive travel planning experience where a user can:

    Look up available flights to a destination

    Set preferences (like time of day, seat type)

    Book a flight

    Cancel a booking

    Monitor the status and weather at the destination

🧱 Architecture:

    Modular Agent Design: Each task is handled by a separate agent class:

        FlightLookupAgent: Searches flights

        FlightBookingAgent: Books flights

        FlightCancellationAgent: Cancels bookings

        FlightMonitoringAgent: Tracks status/weather

        PreferenceAgent: Gathers user preferences

        OrchestratorAgent: Coordinates everything through user interaction

    Data Layer: Static flight data and bookings are held in data.py.

    Tool Layer: Utility functions like weather fetching and flight lookup are in tools.py.

🧠 Features:

    Simulates real-world travel agent behavior

    Input-driven preferences (time, seat)

    Bookings and cancellations stored in memory

    Mock weather data integration

    Status updates based on simple conditions (price = delayed or not)

    Clean CLI-based user interaction