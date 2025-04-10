# ✈️ Travel Assistant

A **Python-based travel planner** built with **Streamlit** that allows users to **search**, **book**, **cancel**, and **monitor** real-time flights. It integrates with **AviationStack** for flight data and **WeatherAPI.com** for weather updates. All bookings are stored in **SQLite** for persistent access.

---

## 🚀 Features

- 🔍 **Search Flights**  
  Find real-time flights between cities using the AviationStack API.

- 🛫 **Book Flights**  
  Select a flight, enter passenger details, and receive a unique ticket ID.

- ❌ **Cancel Bookings**  
  Remove bookings easily using a booking ID.

- 🛰 **Monitor Flights**  
  Track live flight status, destination weather, and potential delays.

- 📡 **Real-Time API Integration**  
  - AviationStack for live flight data  
  - WeatherAPI.com for up-to-date weather info

- 💾 **Persistent Storage**  
  All bookings are saved in an **SQLite database**.

---

## 🔧 Configuration

> No need for `.env` files — API keys are entered directly in the app.

- **AviationStack API Key**  
- **WeatherAPI.com API Key**

Enter both keys in the **Streamlit sidebar** to enable full functionality.

---

## 💻 Usage

### ▶️ Run the Application

```bash
streamlit run main.py
```

> This will open the app at: [http://localhost:8501](http://localhost:8501)

---

### 🔑 Enter API Keys

Use the **sidebar** to input your:

- `AviationStack API Key`
- `WeatherAPI.com API Key`

These keys are required for fetching live **flight** and **weather** data.

---

## 🧭 Explore the Features

### 🔍 Search Flights

- Choose your **departure** and **destination** cities  
- Click **Search** to retrieve live flight options

### 🛫 Book a Flight

1. After searching, select a flight from the list  
2. Click **Proceed to Book**  
3. Enter your **name** and **email**  
4. Click **Confirm Booking**  
5. Receive a **ticket ID**

### ❌ Cancel a Booking

- Enter your **ticket ID**  
- Click **Cancel Booking** to remove it from the database

### 🛰 Monitor a Flight

- Enter your **ticket ID**  
- View real-time:
  - Flight status  
  - Destination weather  
  - Any delay alerts

---

