import requests
import pandas as pd
from datetime import datetime
import os  # Modul tambahan untuk membuat folder dan mengatur jalur file

# latitude dan longitude untuk lokasi yang diinginkan
loc_lat = 1.400221
loc_lon = 124.884608

def get_loc_name(lat,lon):
    """Convert the latitude and longitude into city using OpenStreeetMap."""
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"

    headers = {"User-Agent": "WeatherToExcelScript/1.0 (Python)"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        address = data.get("address", {})

        city = address.get("city") or address.get("town") or address.get("village") or address.get("county")
        country = address.get("country", "")

        if city and country:
            return f"{city}, {country}"
        elif city:
            return city
        else:
            return data.get("display_name", f"{lat}, {lon}")

    except Exception as e:
        print(f"Warning: Could not fetch location name. Error: {e}")
        return f"Lat: {lat}, Lon: {lon}"

def get_wtr_desc(code):
    """Translate standard WMO weather codes into human-readable text."""
    wmo_codes = {
        0: "Langit cerah",
        1: "Sebagian besar cerah", 2: "Cerah berawan", 3: "Mendung",
        45: "Kabut", 48: "Kabut es",
        51: "Gerimis ringan", 53: "Gerimis sedang", 55: "Gerimis lebat",
        56: "Gerimis beku ringan", 57: "Gerimis beku lebat",
        61: "Hujan ringan", 63: "Hujan sedang", 65: "Hujan lebat",
        66: "Hujan beku ringan", 67: "Hujan beku lebat",
        71: "Salju ringan", 73: "Salju sedang", 75: "Salju lebat",
        77: "Butiran salju",
        80: "Hujan lokal ringan", 81: "Hujan lokal sedang", 82: "Hujan lokal sangat lebat",
        85: "Hujan salju ringan", 86: "Hujan salju lebat",
        95: "Badai petir", 96: "Badai petir dengan hujan es ringan", 99: "Badai petir dengan hujan es lebat"
    }
    return wmo_codes.get(code, "Unknown Condition")

def fetch_detailed_wtr(lat, lon):
    loc_name = get_loc_name(lat, lon)
    print(f"Get 10 day forecast for: {loc_name}...")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "apparent_temperature_max",
            "precipitation_sum",
            "precipitation_probability_max",
            "windspeed_10m_max",
            "uv_index_max",
            "weathercode"
        ],
        "timezone": "auto",
        "forecast_days": 10
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    daily_data = response.json()["daily"]

    df = pd.DataFrame(daily_data)
    df["Timestamp"] = pd.to_datetime(df["time"])

    df.insert(1, "Day", df["Timestamp"].dt.day_name())
    df.insert(2, "Location", loc_name)
    df.insert(3, "Weather Description", df["weathercode"].apply(get_wtr_desc))

    df.drop(columns=["weathercode"], inplace=True)

    df.rename(columns={
        "time": "Tanggal",
        "temperature_2m_max": "Max Temp (°C)",
        "temperature_2m_min": "Min Temp (°C)",
        "apparent_temperature_max": "Feel Like Max (°C)",
        "precipitation_sum": "Precipitation (mm)",
        "precipitation_probability_max": "Kemungkinan Hujan (%)",
        "windspeed_10m_max": "Kecepatan Angin Maksimum (km/h)",
        "uv_index_max": "Indeks UV Maksimum"
    }, inplace=True)

    return df, loc_name

if __name__ == "__main__":
    loc_lat = 1.400221
    loc_lon = 124.884608
    weather_df, loc_name = fetch_detailed_wtr(loc_lat, loc_lon)

    # 1. Mengambil nama kota saja untuk dijadikan nama folder (memotong teks sebelum koma)
    folder_name = loc_name.split(',')[0].strip()
    
    # 2. Membuat folder jika belum ada
    # exist_ok=True memastikan program tidak error jika folder sudah pernah dibuat sebelumnya
    os.makedirs(folder_name, exist_ok=True)

    cleaned_loc_name = loc_name.replace(" ", "_").replace(",", "")
    
    # MENDAPATKAN JAM DAN MENIT SAAT INI (Format: HHMM)
    current_time = datetime.now().strftime("%H%M")
    
    # 3. Menyiapkan nama file dan menggabungkannya dengan jalur folder
    file_name = f"{cleaned_loc_name}_10_day_forecast_{current_time}.xlsx"
    output_path = os.path.join(folder_name, file_name)
    
    # 4. Menyimpan file ke dalam jalur yang sudah ditentukan (di dalam folder)
    weather_df.to_excel(output_path, index=False)

    print(f"Sukses! Prakiraan cuaca telah disimpan ke dalam folder '{folder_name}' dengan nama file {file_name}.")

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(weather_df.head(3))