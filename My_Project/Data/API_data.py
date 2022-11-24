# Project: Investment Game

# Import packages (if needed, first install in terminal -- command prompt with: pip install <packagename>
import requests
import pandas as pd

# Import dataset from alphavantage (INTRADAY only covers 2 months, instead we can use time_series_daily)
response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&outputsize=full&apikey=demo")
if response.status_code != 200:
    raise ValueError("Could not retrieve data, code:", response.status_code)

# Transform data from json to python structure
raw_data = response.json()

# Explore data
print(raw_data.keys())
print(raw_data['Meta Data'])
print(raw_data['Time Series (5min'])

# Transform time series data into dataframe
data = raw_data['Time Series (5min)']
df = pd.DataFrame(data).T.apply(pd.to_numeric)

# Fix the column names and specify the index as date time type
df.index = pd.DatetimeIndex(df.index)
df.rename(columns=lambda s: s[3:], inplace=True)

# Ask input for the investment program
numstocks = int(input("How many stocks do you want to buy?"))
buydate = pd.Timestamp("What time and day do you want to buy?")
selldate = pd.Timestamp("What time and day do you want to sell?")

# Calculate the output values (currency to be added)
df['totalprice'] = df['close'] * numstocks
print("Your total investment for", numstocks, "stocks is", df.loc[buydate, "totalprice"], buydate)
print("The price if you sell on", selldate, "is", df.loc[selldate, "totalprice"])
print("The return if you sell on", selldate, "is", (df.loc[selldate, "totalprice"] -
      df.loc[buydate, "totalprice"]), "which is a",
      (((df.loc[selldate, "totalprice"] - df.loc[buydate, "totalprice"]) - df.loc[buydate, "totalprice"]) /
      df.loc[buydate, "totalprice"]) * 100, "percent change"
      )







