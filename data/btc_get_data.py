import yfinance as yf
import pandas as pd

# Fetch full historical data for Bitcoin (BTC-USD)
btc_data = yf.download("BTC-USD", start="2010-01-01")

# Save the data to a CSV file in the './data/' directory. Ensure the directory exists or adjust the path as needed.
btc_data.to_csv('./data/btc_price_history.csv')
