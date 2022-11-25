# Project: Investment Game

# Import packages (if needed, first install in terminal -- command prompt with: pip install <packagename>
import requests
import pandas as pd
import inquirer
from inquirer.themes import GreenPassion

# Use a personal KEY (requested via https://www.alphavantage.co/support/#api-key)
privatekey = "YRX7910M3YV16XQB"

# Lookup what stock you want to buy and get the symbol
keyword = input("Enter company name")

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
col_list = dftop.name.values.tolist()

# Ask user to select a symbol and use as input for next API request
questions = [
  inquirer.List('symbol',
                message="What stock do you need?",
                choices=col_list
                )
]

inquirer.prompt(questions, theme=GreenPassion())

# Retrieve the data of the stock that was selected
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={privatekey}"

response = requests.get(url)
if response.status_code != 200:
    raise ValueError("Could not retrieve data, code:", response.status_code)

