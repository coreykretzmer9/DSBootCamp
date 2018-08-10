
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime as dt

# Import API key, it isn't working for some reason...  Had to manually enter and save.
from api_keys import api_key
api_key = "95fc7d255fb5e201f52e50459432f611"
# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)
print(api_key)

## Generate Cities List

# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)

## Perform API Calls

# OpenWeatherMap API Key

# Starting URL for Weather Map API Call
base_url = "http://api.openweathermap.org/data/2.5/weather?units=Imperial&APPID="

query_url = base_url + api_key + "&q="

# Create empty lists to hold the results of all the values we want for corresponding lat/long
Results = []
City_Name = []
Country = []
Latitude = []
Longitude = []
Humidity = []
Max_Temperature = []
Cloudiness = []
Wind_Speed = []
Date_Time = []

for city in cities:
    # Sleep to prevent denial of access..
    # arg is in seconds
    time.sleep(0.1)
    city_url = query_url + city.replace(" ", "+")
    city_data = requests.get(city_url).json()
    print(f"Retrieving data for {city}")
    print()
    city_id = city_data.get('id')
    if city_data.get("id"):
        print(f"   Record found for City: {city}    City ID: {city_id}")
        print(city_url)
        Results.append(city_data)
        City_Name.append(city_data['name'])
        Country.append(city_data['sys']['country'])
        Latitude.append(city_data['coord']['lat'])
        Longitude.append(city_data['coord']["lon"])
        Humidity.append(city_data['main']['humidity'])
        Max_Temperature.append(city_data['main']['temp_max'])
        Cloudiness.append(city_data['clouds']['all'])
        Wind_Speed.append(city_data['wind']['speed'])
        Date_Time.append(city_data['dt'])
        print()
    elif city_data['cod'] == '404':
        print(f'No data found for city: {city}')
        print()
    print()

print()
print(f"Data Retrieval Complete")
            
#for city in cities:
#    print(f"Retrieving data for {city}:")
#    print()
    


weather = {"Latitude": Latitude, "Longitude": Longitude, 
           "City": City_Name, "Country": Country, 
           "Temperature (F)": Max_Temperature, 
           "Humidity (%)": Humidity, "Cloudiness (%)": Cloudiness, 
           "Wind Speed (mph)": Wind_Speed}

weather_df = pd.DataFrame(weather)
weather_df.to_csv('city_weather.csv')
weather_df.head()

above_eq = weather_df.loc[weather_df['Latitude'] > 0]
below_eq = weather_df.loc[weather_df['Latitude'] < 0]

num_above = len(above_eq)
num_below = len(below_eq)

print(f"Of our sample cities, {num_above} are above the equator.")
print(f"Of our sample cities, {num_below} are below the equator.")

date_time = dt.now().strftime("%H:%M:%S    %m/%d/%Y")
print(date_time)

# Show a scatter of long/lat to visualize where cities samples are located

longs_lats = plt.scatter(weather_df['Longitude'], weather_df['Latitude'], c='blue',
                        marker='^', s=10, alpha=1)
plt.title(f'Sample city distribution {date_time}')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.xlim(-180, 180)
plt.ylim(-90, 90)
plt.grid()
plt.axhline(color='r')
plt.xticks(np.arange(-180, 190, 30))


# Temp vs latitude

temp_lats = plt.scatter(weather_df['Latitude'], weather_df['Temperature (F)'],
                       c='blue', marker="o", s=5)
plt.grid()
plt.title(f'City max temp vs latitude')
plt.xlabel('Latitude')
plt.ylabel('Temperature (F)')
plt.xticks(np.arange(-90, 100, 20))
plt.yticks(np.arange(0, 130, 20))

# Humidity vs latitude

hum_lats = plt.scatter(weather_df['Latitude'], weather_df['Humidity (%)'], 
                      s=10, color='blue', marker='o')

plt.grid()
plt.ylabel('Humidity %')
plt.xlabel('Latitude')
plt.xticks(np.arange(-90, 100, 20))
plt.yticks(np.arange(0, 110, 20))
plt.title(f'City humidity by latitude')

# Cloudiness by latitude

cloud_lats = plt.scatter(weather_df['Latitude'], weather_df['Cloudiness (%)'], 
                      s=10, color='blue', marker='o')

plt.grid()
plt.ylabel('Cloudiness %')
plt.xlabel('Latitude')
plt.xticks(np.arange(-90, 100, 20))
plt.yticks(np.arange(0, 110, 20))
plt.title(f'City cloudiness by latitude')

# Wind speed by latitude

wind_lats = plt.scatter(weather_df['Latitude'], weather_df['Wind Speed (mph)'], 
                      s=10, color='blue', marker='o')

plt.grid()
plt.ylabel('Wind Speed (mph)')
plt.xlabel('Latitude')
plt.xticks(np.arange(-90, 100, 20))
plt.yticks(np.arange(0, 50, 5))
plt.title(f'City wind speed by latitude')

Observations

1. No correlation between latitude and cloudiness
2. Max temp is higher in locations above the equator, not at the equator, which isn't what I'd expected.
3. No correlation between wind speed and latitude.
4. I forgot to do these observations, and now it's 10 PM on the night this assignment is due.  Sorry these are not very insightful.