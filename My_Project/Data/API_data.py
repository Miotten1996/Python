# Project: Investment Game

# Import packages (if needed, first install in terminal -- command prompt with: pip install <packagename>
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Import dataset from alphavantage (INTRADAY only covers 2 months, instead we can use time_series_daily)
#response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&outputsize=full&apikey=demo")
#if response.status_code != 200:
 #   raise ValueError("Could not retrieve data, code:", response.status_code)

response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=demo")
if response.status_code != 200:
    raise ValueError("Could not retrieve data, code:", response.status_code)

# Transform data from json to python structure
raw_data = response.json()

# Explore data
print(raw_data.keys())
print(raw_data['Meta Data'])
print(raw_data['Time Series (Daily)'])


# Transform time series data into dataframe
data = raw_data['Time Series (Daily)']
df = pd.DataFrame(data).T.apply(pd.to_numeric)


# print length of df number of rows = 5805
print(df.shape[0])

# Fix the column names and specify the index as date time type
df.index = pd.DatetimeIndex(df.index)
df.index = df.index.strftime("%m-%d-%Y")
print(df)
df.rename(columns=lambda s: s[3:], inplace=True)

#create a plot: >> totalprice plotten
#fig, ax = plt.subplots()
#plot = df[['open', 'high', 'low', 'close']].plot(ax=ax)
#plt.show()

#CREATE NEW COLUMNS
df['totalprice'] = df['close']*df['volume']
print(df)

#create a plot: >> totalprice plotten
fig, ax = plt.subplots()
plot = df[['totalprice']].plot(ax=ax)
plt.show()


#search first and last date
Firsdate = (str(df.index[-1]))
Lastdate = (str(df.index[0]))

# Ask input for the investment program
cashbalance= int(input('What is your cashbalance'))
numstocks = int(input("How many stocks do you want to buy?"))
print("For the next questions, please fill a date between", Firsdate, "and", Lastdate)
buydate = pd.Timestamp(input("What day do you want to buy? Fill a date"))
selldate = pd.Timestamp(input("What day do you want to sell? Fill a date"))

# Calculate the output values (currency to be added)
df['totalprice'] = df['close'] * numstocks
totalprice = df.loc[buydate, 'close'] * numstocks

print("Your total investment for", numstocks, "stocks is", df.loc[buydate, "totalprice"], "if you buy on", buydate) #df = lookup in df
print("The price if you sell on", selldate, "is $", df.loc[selldate, "totalprice"])
print("The return if you sell on", selldate, "is $", round((df.loc[selldate, "totalprice"] -
      df.loc[buydate, "totalprice"]),6), "which is a",
     round((df.loc[selldate, "totalprice"] - df.loc[buydate, "totalprice"]) /
      df.loc[buydate, "totalprice"], 6)* 100, "%"
      )
print('Your current cashbalance is $', cashbalance - df.loc[buydate, "totalprice"]+ df.loc[selldate, "totalprice"])



# add statement if the cashbalance below 0 then send an message your cashbalance is less then your total investment
# add currency to selldate #Shenyu #done

# change number formatting: 2/3 numbers after comma #Shenyu#done

# look at range of dates & add condition in input statement ("fill date between xx and xx") #Michelle

# adjust url with multiple stocks (Quote endpoint) - write input statement where you can select a stockname #Susanne

# Insert your cashbalance > update the cashbalance with how much money they lost or won #Together - Michelle
# line 40 change the columns


# Change date formats to Month date year --> check (Michelle)

#remove time in code --> check (Michelle)

#Create plot obv notebook --> example notebook









