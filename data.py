# data.py

# Enhanced static flight data (mock database)
flights = [
    {
        "id": 1,
        "airline": "Delta",
        "departure": "Chicago",
        "destination": "New York",
        "time": "08:00",
        "duration": "2h 30m",
        "price": 200,
        "seats": {"economy": 10, "business": 4}
    },
    {
        "id": 2,
        "airline": "United",
        "departure": "Chicago",
        "destination": "New York",
        "time": "14:00",
        "duration": "2h 45m",
        "price": 250,
        "seats": {"economy": 8, "business": 2}
    },
    {
        "id": 3,
        "airline": "British Airways",
        "departure": "New York",
        "destination": "London",
        "time": "10:00",
        "duration": "7h 15m",
        "price": 450,
        "seats": {"economy": 15, "business": 5}
    },
    {
        "id": 4,
        "airline": "EasyJet",
        "departure": "New York",
        "destination": "London",
        "time": "16:00",
        "duration": "7h 30m",
        "price": 300,
        "seats": {"economy": 20, "business": 3}
    },
    {
        "id": 5,
        "airline": "Southwest",
        "departure": "Los Angeles",
        "destination": "San Francisco",
        "time": "09:30",
        "duration": "1h 20m",
        "price": 120,
        "seats": {"economy": 12, "business": 0}  # No business class
    },
    {
        "id": 6,
        "airline": "American",
        "departure": "Los Angeles",
        "destination": "San Francisco",
        "time": "13:00",
        "duration": "1h 15m",
        "price": 150,
        "seats": {"economy": 10, "business": 2}
    },
    {
        "id": 7,
        "airline": "Emirates",
        "departure": "San Francisco",
        "destination": "Dubai",
        "time": "18:00",
        "duration": "16h 10m",
        "price": 900,
        "seats": {"economy": 25, "business": 8}
    },
    {
        "id": 8,
        "airline": "Qatar Airways",
        "departure": "Chicago",
        "destination": "Dubai",
        "time": "20:00",
        "duration": "14h 50m",
        "price": 850,
        "seats": {"economy": 18, "business": 6}
    }
]

# In-memory booking store (unchanged)
bookings = {}