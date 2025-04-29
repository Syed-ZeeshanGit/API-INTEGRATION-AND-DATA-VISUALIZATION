# weather_dashboard.py 

import requests
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import sys
import os

# Set Seaborn style
sns.set(style="whitegrid")

# 1. Function to fetch weather data
def fetch_weather_data(city_name, api_key):
    URL = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric"
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        sys.exit(1)
    except Exception as err:
        print(f"An error occurred: {err}")
        sys.exit(1)

# 2. Function to process weather data
def process_weather_data(data):
    times = []
    temperatures = []
    humidity = []

    for entry in data['list']:
        times.append(datetime.datetime.fromtimestamp(entry['dt']))
        temperatures.append(entry['main']['temp'])
        humidity.append(entry['main']['humidity'])

    return times, temperatures, humidity

# 3. Function to create and save visualizations
def create_visualizations(times, temperatures, humidity, city_name):
    # Ensure output folder exists
    output_dir = "weather_graphs"
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(14, 6))

    # Temperature plot
    plt.subplot(1, 2, 1)
    sns.lineplot(x=times, y=temperatures, marker="o", color="red")
    plt.title(f"Temperature Trend in {city_name}")
    plt.xlabel("Date and Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)

    # Humidity plot
    plt.subplot(1, 2, 2)
    sns.lineplot(x=times, y=humidity, marker="o", color="blue")
    plt.title(f"Humidity Trend in {city_name}")
    plt.xlabel("Date and Time")
    plt.ylabel("Humidity (%)")
    plt.xticks(rotation=45)

    plt.tight_layout()

    # Save the figure
    filename = f"{output_dir}/{city_name}_weather.png"
    plt.savefig(filename, dpi=300)
    print(f"✅ Graphs saved as '{filename}'")

    # Also show the plot
    plt.show()

# 4. Main function
def main():
    print("=== Weather Dashboard (Bonus Version) ===")
    city_name = input("Enter the city name: ")
    api_key = '759a48467afcba27e7b0c381154437f0'

    # Fetch data
    data = fetch_weather_data(city_name, api_key)

    # Validate city
    if data['cod'] != '200':
        print(f"City {city_name} not found. Please check the spelling.")
        sys.exit(1)

    # Process and visualize
    times, temperatures, humidity = process_weather_data(data)
    create_visualizations(times, temperatures, humidity, city_name)

if __name__ == "__main__":
    main()
