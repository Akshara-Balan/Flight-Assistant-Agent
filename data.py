# data.py
import sqlite3

def init_db():
    conn = sqlite3.connect("travel.db")
    c = conn.cursor()
    
    # Updated bookings table with departure and destination
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        flight_id TEXT,
        seat_type TEXT,
        passenger_name TEXT,
        passenger_email TEXT,
        ticket_id TEXT,
        departure TEXT,
        destination TEXT
    )''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()