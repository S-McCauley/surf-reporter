import time
import os
import requests
import pyfiglet

# --- Fetch Swell Height ---
def fetch_swell_height_feet():
    url = "https://www.ndbc.noaa.gov/data/realtime2/41004.txt"
    try:
        response = requests.get(url, timeout=10)
        lines = response.text.strip().split("\n")
        for line in lines:
            if not line.startswith("#"):
                parts = line.split()
                swell_height_m = parts[8]
                if swell_height_m != "MM":
                    return float(swell_height_m) * 3.28084
    except:
        return None
    return None

# --- Full-Screen Terminal Dashboard ---
def dashboard():
    update_interval = 600  # 10 minutes
    last_update = 0
    swell = 0.0
    ascii_height = pyfiglet.figlet_format("No Data", font="standard", justify="center")

    while True:
        # Update swell every 10 minutes
        if time.time() - last_update >= update_interval:
            new_swell = fetch_swell_height_feet()
            if new_swell is not None:
                swell = new_swell
                # Use a classic ASCII font
                ascii_height = pyfiglet.figlet_format(
                    f"{swell:.2f} ft", font="standard", justify="center")
            last_update = time.time()

        # Clear terminal for full-widget effect
        os.system("cls" if os.name == "nt" else "clear")

        # Print title and ASCII-art height
        print("\nFolly Beach Swell\n".center(100))
        print(ascii_height)

        time.sleep(60)

if __name__ == "__main__":
    dashboard()

