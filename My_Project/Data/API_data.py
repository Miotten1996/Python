# Project: Investment Game

# Import packages (if needed, first install in terminal -- command prompt with: pip install <packagename>
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Use a personal KEY (requested via https://www.alphavantage.co/support/#api-key)
privatekey = "YRX7910M3YV16XQB"

# Lookup what stock you want to buy and get the symbol
keyword = input("Enter symbol search word")

url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={privatekey}"
r = requests.get(url)
data = r.json()

# Output is a dictionary called "best matches"[1. symbol 2. name, 3. type, 4. region, 8. currency and 9. matchScore)

# Transform data into dataframe
targetdata = data['bestMatches']
df = pd.DataFrame(targetdata)

# Change datatypes and sort on highest match score
df['9. matchScore'] = pd.to_numeric(df['9. matchScore'])
df.rename(columns=lambda s: s[3:], inplace=True)
df.sort_values(by='matchScore', ascending=False, na_position='last')

# Select top results
dftop = df.nlargest(30, "matchScore")

print(f"Your search results for the keyword {keyword} are:")
print(dftop)

symbolrow = int(input("Enter the row number of the symbol you want to use from the list above"))

symbol = df.iloc[symbolrow, 0]

# Retrieve the data of the stock that was selected
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={privatekey}"


# Import dataset from alphavantage time_series_daily adjusted
response = requests.get(url)
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
df.index = df.index.strftime("%d-%m-%Y")
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
ax.set_title('Total value of stocks over time')
ax.set_ylabel('Total price x100.000.000')
plot.invert_xaxis()
ax.set_xlabel('buy-date')
plt.show() #hierna window sluiten

#search first and last date
Firsdate = (str(df.index[-1]))
Lastdate = (str(df.index[0]))
print(Firsdate)
print(Lastdate)

# Ask input for the investment program
cashbalance= int(input('What is your cashbalance'))
numstocks = int(input("How many stocks do you want to buy?"))
print("For the next questions, please fill a date between", Firsdate, "and", Lastdate)
buydate = (input("What day do you want to buy? Fill a date"))
selldate = (input("What day do you want to sell? Fill a date"))

# Calculate the output values (currency to be added)
df['totalprice'] = df['close'] * numstocks
totalprice = df.loc[buydate, 'close'] * numstocks

print("Your total investment for", numstocks, "stocks is", round(df.loc[buydate, "totalprice"], 6),"if you buy on", buydate) #df = lookup in df
print("The price if you buy on", buydate, "is $", round(df.loc[buydate, "totalprice"],6))
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

#Create plot obv notebook --> example notebook (Michelle)--> Y-as aanpassen

# Create class












