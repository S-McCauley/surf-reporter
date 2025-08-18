import time
import requests
from prometheus_client import start_http_server, Gauge

# --- Prometheus Metrics ---
wave_height_m_gauge = Gauge('wave_height_m', 'Wave height in meters')
wave_height_ft_gauge = Gauge('wave_height_ft', 'Wave height in feet')
wind_speed_gauge = Gauge('wind_speed_mps', 'Wind speed in m/s')
wind_gust_gauge = Gauge('wind_gust_mps', 'Wind gust in m/s')
wind_dir_gauge = Gauge('wind_direction_deg', 'Wind direction in degrees')
dominant_period_gauge = Gauge('dominant_wave_period_sec', 'Dominant wave period in seconds')
average_period_gauge = Gauge('average_wave_period_sec', 'Average wave period in seconds')
wave_dir_gauge = Gauge('wave_direction_deg', 'Wave direction in degrees')
pressure_gauge = Gauge('pressure_hpa', 'Atmospheric pressure in hPa')
temp_surface_gauge = Gauge('sea_surface_temp_c', 'Sea surface temperature in °C')
temp2_gauge = Gauge('temp2_c', 'Water temp sensor 2 in °C')
temp3_gauge = Gauge('temp3_c', 'Water temp sensor 3 in °C')
visibility_gauge = Gauge('visibility_nmi', 'Visibility in nautical miles')
pressure2_gauge = Gauge('pressure2_hpa', 'Secondary pressure in hPa')

# --- Fetch NOAA Data ---
def fetch_buoy_data():
    url = "https://www.ndbc.noaa.gov/data/realtime2/41004.txt"
    try:
        response = requests.get(url, timeout=10)
        lines = response.text.strip().split("\n")
        for line in lines:
            if not line.startswith("#"):
                parts = line.split()
                
                # Parse and convert values
                wave_height_m = float(parts[8]) if parts[8] != "MM" else None
                wave_height_ft = wave_height_m * 3.28084 if wave_height_m else None
                wind_speed_mps = float(parts[6]) if parts[6] != "MM" else None
                wind_gust_mps = float(parts[7]) if parts[7] != "MM" else None
                wind_dir_deg = float(parts[5]) if parts[5] != "MM" else None
                dominant_period_sec = float(parts[9]) if parts[9] != "MM" else None
                average_period_sec = float(parts[10]) if parts[10] != "MM" else None
                wave_dir_deg = float(parts[11]) if parts[11] != "MM" else None
                pressure_hpa = float(parts[12]) if parts[12] != "MM" else None
                temp_surface_c = float(parts[13]) if parts[13] != "MM" else None
                temp2_c = float(parts[14]) if parts[14] != "MM" else None
                temp3_c = float(parts[15]) if parts[15] != "MM" else None
                visibility_nmi = float(parts[16]) if parts[16] != "MM" else None
                pressure2_hpa = float(parts[17]) if parts[17] != "MM" else None

                # Update Prometheus metrics
                if wave_height_m: wave_height_m_gauge.set(wave_height_m)
                if wave_height_ft: wave_height_ft_gauge.set(wave_height_ft)
                if wind_speed_mps: wind_speed_gauge.set(wind_speed_mps)
                if wind_gust_mps: wind_gust_gauge.set(wind_gust_mps)
                if wind_dir_deg: wind_dir_gauge.set(wind_dir_deg)
                if dominant_period_sec: dominant_period_gauge.set(dominant_period_sec)
                if average_period_sec: average_period_gauge.set(average_period_sec)
                if wave_dir_deg: wave_dir_gauge.set(wave_dir_deg)
                if pressure_hpa: pressure_gauge.set(pressure_hpa)
                if temp_surface_c: temp_surface_gauge.set(temp_surface_c)
                if temp2_c: temp2_gauge.set(temp2_c)
                if temp3_c: temp3_gauge.set(temp3_c)
                if visibility_nmi: visibility_gauge.set(visibility_nmi)
                if pressure2_hpa: pressure2_gauge.set(pressure2_hpa)
                
                # Only use the first valid data line
                break
    except Exception as e:
        print(f"Error fetching buoy data: {e}")

# --- Main Loop ---
if __name__ == "__main__":
    start_http_server(8000)  # Prometheus scraping endpoint
    update_interval = 600     # Fetch every 10 minutes

    while True:
        fetch_buoy_data()
        time.sleep(update_interval)

