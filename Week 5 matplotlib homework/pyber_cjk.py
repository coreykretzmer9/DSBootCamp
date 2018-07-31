
1. It makes sense - and is shown - that there are fewer rides in rural towns/cities than there are in urban or suburban areas.  However, it is also shown that the rides end up being more costly for those riders in rural areas, presumably due to the longer distances traveled in Pyber.
2. It would be interesting to see how "profitable" rides are at an hourly rate, we would need the start AND end times to determine these figures; alternatively, maybe the mileage traveled in each ride? - not really an observation...
3. This is a relatively small n-size for drivers, with 52 drivers comprising the entire driver-pool between three areas.  Individual drivers are also not limited individual townships, urban or otherwise, so there is overlap here. - not really an observation, either...
4. With fewer drivers and less "crowded" areas of patronage, there tend to be higher average fares per ride.
5. There are more users in urban settings, but there may be a trade-off in profitability when there are more riders driving for shorter distances, compared to in rural settings where fewer riders are traveling significantly longer distances.


%matplotlib inline
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

# File to Load (Remember to change these)
city_data_to_load = "data/city_data.csv"
ride_data_to_load = "data/ride_data.csv"

# Read the City and Ride Data
cityRead = pd.read_csv(city_data_to_load)
rideRead = pd.read_csv(ride_data_to_load)

# Combine the data into a single dataset
ridesCombined = cityRead.merge(rideRead, on="city", how="outer")

ridesCombined.head()

# Find total number of drivers by dropping duplicates based on driver ID.
droppedRidesCombined = ridesCombined.drop_duplicates('driver_count', keep="first")
droppedRidesCombined['driver_count'].count()

# Create separate datasets for each city-type (Urban, Suburban, Rural)
uRides = ridesCombined[ridesCombined["type"] == "Urban"]
sRides = ridesCombined[ridesCombined["type"] == "Suburban"]
rRides = ridesCombined[ridesCombined["type"] == "Rural"]

# Urban Fare, Urban City Rides, Urban City Drivers
uAverageFare = uRides.groupby('city')['fare'].mean()
uCityRides = uRides.groupby('city')['ride_id'].count()
#uTotalCityDrivers = uRidesDropped.groupby('city')['driver_count'].value_counts()
uTotalCityDrivers = uRides.groupby('city')['driver_count'].value_counts()

# Suburban Fare,  city rides, drivers
sAverageFare = sRides.groupby('city')['fare'].mean()
sCityRides = sRides.groupby('city')['ride_id'].count()
#sTotalCityDrivers = sRidesDropped.groupby('city')['driver_count'].value_counts()
sTotalCityDrivers = sRides.groupby('city')['driver_count'].value_counts()

# Rural fare, city rides, drivers
rAverageFare = rRides.groupby('city')['fare'].mean()
rCityRides = rRides.groupby('city')['ride_id'].count()
#rTotalCityDrivers = rRidesDropped.groupby('city')['driver_count'].value_counts()
rTotalCityDrivers = rRides.groupby('city')['driver_count'].value_counts()


plt.scatter(uCityRides, 
            uAverageFare, 
            s=10*uTotalCityDrivers, color="gold",
            edgecolor="black", linewidths=0.5, marker="o",
            alpha=1, label="Urban")

plt.scatter(sCityRides, 
            sAverageFare, 
            s=10*sTotalCityDrivers, color="lightskyblue",
            edgecolor="black", linewidths=0.5, marker="o",
            alpha=1, label="Suburban")

plt.scatter(rCityRides, 
            rAverageFare, 
            s=10*rTotalCityDrivers, color="lightcoral", 
            edgecolor="black", linewidths=0.5, marker="o",
            alpha=1, label="Rural")

plt.grid(True, alpha=0.4)
plt.title('Pyber 2018 Ride Sharing Data, Average Fare by City and City Type')
plt.xlabel('Number of Rides')
plt.ylabel('Average Ride Fare')
plt.xlim(0, max(uCityRides) + 5)
plt.ylim(min(uAverageFare) - 5, max(rAverageFare) + 5)

legnd = plt.legend(loc="best", title="City Types", fontsize="small", shadow=True)
legnd.legendHandles[0]._sizes=[75]
legnd.legendHandles[1]._sizes=[75]
legnd.legendHandles[2]._sizes=[75]

plt.show()

## Total Fares by City Type

cityPieFare = ridesCombined.groupby('type')['fare'].sum()

cityPieFare

plt.pie(cityPieFare, startangle = 90, colors = ['gold', 'lightskyblue', 'lightcoral'], explode=(0, 0, 0.1), labels=cityPieFare.index, 
labeldistance=1.1, radius=1, autopct = "%1.2f%%", pctdistance=0.7)
plt.axis('equal')
plt.title('% of Total Fares by City Type')

## Total Rides by City Type

cityPieRides = ridesCombined.groupby('type')['ride_id'].count()
cityPieRides

plt.pie(cityPieRides, startangle = 90, colors = ['gold', 'lightskyblue', 'lightcoral'], explode=(0, 0, 0.1), labels=cityPieRides.index, 
labeldistance=1.1, radius=1, autopct = "%1.2f%%", pctdistance=0.7)
plt.axis('equal')
plt.title('% of Total Rides by City Type')

## Total Drivers by City Type

# There are only a total of 52 drivers across all cities!
cityPieDrivers = droppedRidesCombined.groupby('type')['driver_count'].count()
cityPieDrivers

plt.pie(cityPieDrivers, startangle = 90, colors = ['gold', 'lightskyblue', 'lightcoral'], labels=cityPieDrivers.index, 
labeldistance=1.1, radius=1, autopct = "%1.2f%%", pctdistance=0.7)
plt.axis('equal')
plt.title('% of Total Rides by City Type')