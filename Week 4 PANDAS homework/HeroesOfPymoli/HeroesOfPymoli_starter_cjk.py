### Note
#* Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.



# Dependencies and Setup
import pandas as pd
import numpy as np
import decimal as Decimal
import os
import csv

# Raw data file
file_to_load = "Resources/purchase_data.csv"

# Read purchasing file and store into pandas data frame
purchase_data = pd.read_csv(file_to_load)
purchase_data.head()

# Drop duplicates based off of unique 'SN'
purchase_data_dropped = purchase_data.drop_duplicates(['SN'], keep='last')

## Player Count

#* Display the total number of players


totalPlayers = purchase_data_dropped["Purchase ID"].count()
print("Total player count is " + str(totalPlayers) + ", predominantly male, players.  This excludes duplicate purchases.")

purchase_data_dropped["Gender"].unique()

purchase_data_dropped.head()

## Purchasing Analysis (Total)

'''* Run basic calculations to obtain number of unique items, average price, etc.


* Create a summary data frame to hold the results


* Optional: give the displayed data cleaner formatting


* Display the summary data frame
'''

# This will identify how many unique values there are in the "item name" column, append them to a new list, then we count the length of the list to get the total unique item amount.
uniqueItems = len(purchase_data["Item Name"].unique())

# This will spit out the average of all values within the "Price" column.
avgPrice = purchase_data["Price"].mean()

# Total number of purchases will be found exmamining the non-dropped dataframe
totalPurchases = purchase_data["Purchase ID"].count()
# Total revenue is the summation of the "Prices" column
totalRevenue = purchase_data["Price"].sum()

# Need to convert prices column and all columns calculated from that original column to currency, so, we convert floats to currency format with 2
pd.options.display.float_format = '${:,.2f}'.format

# We need to set all of these values within a new, summary, data frame.
# Need to format Average Price and Total Revenue as $$$ and round to two decimal places.
summary_df = pd.DataFrame({"Number of Unique Items" : [uniqueItems], "Average Price" : [avgPrice], "Number of Purchases" : [totalPurchases], "Total Revenue" : [totalRevenue]})

summary_df

## Gender Demographics
'''
* Percentage and Count of Male Players


* Percentage and Count of Female Players


* Percentage and Count of Other / Non-Disclosed
'''



# .map("{:.2f}%").format for the gender percentage column to format as a 2 decimal place percentage value.)
maleCount = purchase_data_dropped['Gender'].value_counts()['Male']
femaleCount = purchase_data_dropped['Gender'].value_counts()['Female']
otherCount = purchase_data_dropped['Gender'].value_counts()['Other / Non-Disclosed']
totalCount = maleCount + femaleCount + otherCount

malePerc = 100 * maleCount / totalCount
femalePerc = 100 * femaleCount / totalCount
otherPerc = 100 * otherCount / totalCount

#totalDic = {"Total Count" : [maleCount, femaleCount, otherCount]}
#percDic = {"Percentage of Players" : [malePerc, femalePerc, otherPerc]}
#genderDic = {"Gender" : ["Male", "Female", "Other / Non-Disclosed"]}

gender_summary_df = pd.DataFrame({"Percentage of Players" : [malePerc, femalePerc, otherPerc], "Total Count" : [maleCount, femaleCount, otherCount]}, index=["Male", "Female", "Other / Non-Disclosed"])
gender_summary_df["Percentage of Players"] = gender_summary_df["Percentage of Players"].map("{:.2f}%".format)

gender_summary_df


## Purchasing Analysis (Gender)
'''
* Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender




* Create a summary data frame to hold the results


* Optional: give the displayed data cleaner formatting


* Display the summary data frame
'''
# Columns: gender(index), Purchase count, average purchase price, total purchase value
gender_index = ["Male", "Female", "Other / Non-Disclosed"]

# Use .loc to search through the instances where each gender is mentioned, tie this together as the total # of gender purchases by finding the len of those lists
male_purchases_loc = purchase_data.loc[(purchase_data["Gender"] =="Male")]
female_purchases_loc = purchase_data.loc[(purchase_data["Gender"] =="Female")]
other_purchases_loc = purchase_data.loc[(purchase_data["Gender"] =="Other / Non-Disclosed")]

male_purchases = len(male_purchases_loc)
female_purchases = len(female_purchases_loc)
other_purchases = len(other_purchases_loc)

# Find total money spent by each gender
male_total_purchases = male_purchases_loc["Price"].sum()
female_total_purchases = female_purchases_loc["Price"].sum()
other_total_purchases = other_purchases_loc["Price"].sum()

# Avg purchase prices
# Refer to the .loc for each gender to find the price paid at each of these index values
avg_male_purchase = male_total_purchases / male_purchases
avg_female_purchase = female_total_purchases / female_purchases
avg_other_purchase = other_total_purchases / other_purchases

gender_purchases_df = pd.DataFrame({"Purchase Count" : [male_purchases, female_purchases, other_purchases],
                                   "Average Purchase Price" : [avg_male_purchase, avg_female_purchase, avg_other_purchase],
                                   "Total Purchase Price" : [male_total_purchases, female_total_purchases, other_total_purchases]},
                                   index=gender_index)
gender_purchases_df

## Age Demographics
'''
* Establish bins for ages
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]
done

* Categorize the existing players using the age bins. Hint: use pd.cut()
done

* Calculate the numbers and percentages by age group


* Create a summary data frame to hold the results


* Optional: round the percentage column to two decimal points


* Display Age Demographics Table
'''

# Establish bins for ages
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]
purchase_data["Age Index"] = pd.cut(purchase_data["Age"], age_bins, labels = group_names)
purchase_data_dropped["Age Index"] = pd.cut(purchase_data["Age"], age_bins, labels=group_names)

#age_grouped = purchase_data_dropped.groupby(["Age Index"])
#for name,group in age_grouped:
#    print(name)
#    print(group)

group_purchases = []
for name in group_names:
    group_purchases.append(len(purchase_data.loc[(purchase_data["Age Index"] == name)]))

group_percentages = []
for purchases in group_purchases:
    group_percentages.append((purchases/sum(group_purchases)) * 100)
    
age_demographics_df =pd.DataFrame({"Percentage of Players" : group_percentages,
                                  "Total Purchase Count" : group_purchases},
                                 index=group_names)

age_demographics_df["Percentage of Players"] = age_demographics_df["Percentage of Players"].map("{:.2f}%".format)

age_demographics_df

## Purchasing Analysis (Age)
'''
* Bin the purchase_data data frame by age


* Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below


* Create a summary data frame to hold the results


* Optional: give the displayed data cleaner formatting


* Display the summary data frame
'''
# Columns: index(Age-group), Purchase Count, Average Purchase Price, Total Purchase Value, Average Purchase Total per Person
# index is our above "group_names" list

# Purchase count is our "group_purchases" list

# Average purchase price
# Need to find the total revenue (price_sum) for the age group, then divide by # of individuals (len(age_group))
# Need to format these as $$
total_group_price = []
for name in group_names:
    total_group_price.append(sum(purchase_data.loc[(purchase_data["Age Index"] == name)]["Price"]))

average_group_price = []
for i in range(len(total_group_price)):
    average_group_price.append(total_group_price[int(i)]/group_purchases[int(i)])

# Average purchase per person is different from average price, since the dropped_duplicate file excludes repeat buyers
average_group_individual_price = []
group_individual_purchases = []
for name in group_names:
    group_individual_purchases.append(len(purchase_data_dropped.loc[(purchase_data["Age Index"] == name)]))

for i in range(len(total_group_price)):
    average_group_individual_price.append(total_group_price[int(i)]/group_individual_purchases[int(i)])

purchasing_analysis_age_summary_df = pd.DataFrame({"Purchase Count" : group_purchases,
                                                  "Average Purchase Price" : average_group_price,
                                                  "Total Purchase Value" : total_group_price,
                                                  "Average Purchase Total / Person" : average_group_individual_price},
                                                 index=group_names)
purchasing_analysis_age_summary_df[["Average Purchase Price","Total Purchase Value"]] = purchasing_analysis_age_summary_df[["Average Purchase Price","Total Purchase Value"]].applymap("${:.2f}".format)
purchasing_analysis_age_summary_df

## Top Spenders
'''
* Run basic calculations to obtain the results in the table below


* Create a summary data frame to hold the results


* Sort the total purchase value column in descending order


* Optional: give the displayed data cleaner formatting


* Display a preview of the summary data frame
'''




# sort by Total Purchase Value
# call summary_df.head(5) to display table similarly to example
# Find spenders, group by "SN" instead of age in this set
# Create an organized df with SN, Purchase Count, Purchase Price

# group based on SN, then figure out which of these bought multiple items and spent most
grouped_df = purchase_data.groupby("SN")

sn_total_purchase = grouped_df['Price'].sum()
sn_purchase_count = grouped_df['Price'].count()
sn_purchase_avg = grouped_df['Price'].mean()

spender_df = pd.DataFrame({"Purchase Count" : sn_purchase_count,
                          "Average Purchase Price" : sn_purchase_avg,
                          "Total Purchase Value" : sn_total_purchase})
spender_df.sort_values(["Total Purchase Value"], ascending=False).head(5)

## Most Popular Items
'''
* Retrieve the Item ID, Item Name, and Item Price columns


* Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value


* Create a summary data frame to hold the results


* Sort the purchase count column in descending order


* Optional: give the displayed data cleaner formatting


* Display a preview of the summary data frame


'''
grouped_df = purchase_data.groupby(["Item ID", "Item Name"])

item_total_price = grouped_df['Price'].sum()
item_purchase_count = grouped_df['Price'].count()
item_price = grouped_df['Price'].max()


popular_df = pd.DataFrame({"Purchase Count" : item_purchase_count,
                          "Item Price" : item_price,
                          "Total Purchase Value" : item_total_price})

popular_df.sort_values(["Purchase Count"], ascending=False).head(5)

## Most Profitable Items
'''
* Sort the above table by total purchase value in descending order


* Optional: give the displayed data cleaner formatting


* Display a preview of the data frame
'''


profitable_df = popular_df.sort_values(["Total Purchase Value"], ascending=False)
profitable_df.head()