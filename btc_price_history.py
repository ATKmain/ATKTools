import yfinance as yf
import pandas as pd

# Fetch historical data for Bitcoin
btc = yf.Ticker("BTC-USD")

# Define the period for historical data, e.g., the last 5 years
btc_hist = btc.history(period="5y")

# Display the data
print(btc_hist)

# Example: Finding the low and high within a specific period
# You would replace 'start_date' and 'end_date' with the cycle start and end dates
start_date = '2020-05-11'
end_date = '2024-05-01'  # Hypothetical end date for illustration

# Filter the historical data for the cycle
cycle_data = btc_hist.loc[start_date:end_date]

# Find the low and high prices in the cycle
low_price = cycle_data['Low'].min()
high_price = cycle_data['High'].max()

print(f"Low Price: {low_price}, High Price: {high_price}")

# With the low and high prices, you could then calculate the percentage range for each month
# This would involve similar logic to the hypothetical code provided, 
# interpolating prices and calculating their relative positions between low and high.

