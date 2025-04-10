# data.py
import sqlite3
from datetime import time


def init_db():
    conn = sqlite3.connect("travel.db")
    c = conn.cursor()
    
    # Create flights table
    c.execute('''CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY,
        airline TEXT,
        departure TEXT,
        destination TEXT,
        time TEXT,
        duration TEXT,
        base_price REAL,
        seats_economy INTEGER,
        seats_business INTEGER,
        legs TEXT
    )''')
    
    # Create bookings table
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        flight_id INTEGER,
        seat_type TEXT,
        price REAL,
        currency TEXT
    )''')
    
    # Insert flight data (20+ departures and destinations)
    flights_data = [
        (1, "Delta", "Chicago", "New York", "08:00", "2h 30m", 200, 10, 4, None),
        (2, "United", "Chicago", "New York", "14:00", "2h 45m", 250, 8, 2, None),
        (3, "British Airways", "New York", "London", "10:00", "7h 15m", 450, 15, 5, None),
        (4, "Emirates", "San Francisco", "Dubai", "18:00", "20h 45m", 900, 25, 8, "San Francisco-Los Angeles-Dubai"),
        (5, "Qatar Airways", "Chicago", "Dubai", "20:00", "18h 50m", 850, 18, 6, "Chicago-Doha-Dubai"),
        (6, "Air India", "Mumbai", "Delhi", "09:00", "2h 10m", 100, 20, 5, None),
        (7, "IndiGo", "Delhi", "Bangalore", "12:00", "2h 45m", 120, 15, 3, None),
        (8, "Japan Airlines", "Tokyo", "Sydney", "15:00", "9h 30m", 600, 12, 4, None),
        (9, "Air France", "Paris", "Berlin", "11:00", "1h 30m", 150, 10, 2, None),
        (10, "Lufthansa", "Berlin", "Toronto", "13:00", "8h 45m", 500, 15, 5, None),
        (11, "Singapore Airlines", "Singapore", "Hong Kong", "16:00", "3h 50m", 300, 20, 6, None),
        (12, "Korean Air", "Seoul", "Tokyo", "09:30", "2h 20m", 200, 18, 4, None),
        (13, "Aeroflot", "Moscow", "Beijing", "17:00", "7h 45m", 400, 15, 3, None),
        (14, "China Eastern", "Shanghai", "Singapore", "14:30", "5h 20m", 350, 12, 5, None),
        (15, "LATAM", "Rio de Janeiro", "Cape Town", "19:00", "12h 30m", 700, 20, 6, None),
        (16, "American", "Los Angeles", "Mumbai", "21:00", "18h 15m", 800, 25, 8, "Los Angeles-Delhi-Mumbai"),
        (17, "SpiceJet", "Bangalore", "Delhi", "08:30", "2h 50m", 110, 15, 3, None),
        (18, "Qantas", "Sydney", "Singapore", "13:30", "8h 10m", 550, 10, 4, None),
        (19, "Emirates", "Dubai", "Paris", "10:30", "7h 20m", 600, 18, 6, None),
        (20, "Air Canada", "Toronto", "London", "15:45", "7h 00m", 450, 12, 5, None),
        (21, "Vistara", "Delhi", "Mumbai", "11:30", "2h 15m", 130, 20, 4, None),
        (22, "ANA", "Tokyo", "Seoul", "12:45", "2h 30m", 220, 15, 3, None),
        (23, "Turkish Airlines", "Istanbul", "Moscow", "16:15", "3h 00m", 250, 18, 5, None),
        (24, "South African", "Cape Town", "Dubai", "20:30", "9h 45m", 650, 15, 6, None),
    ]
    
    c.executemany("INSERT OR IGNORE INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", flights_data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()