import pandas as pd
from pandas.tseries.offsets import DateOffset


# Load the historical Bitcoin data from the saved CSV file
btc_data = pd.read_csv('./data/btc_price_history.csv', index_col='Date', parse_dates=True)


# Example for the 1st halving cycle
halving_date = pd.Timestamp('2012-11-28')

# Calculate start and end dates for the cycle range
start_date = halving_date - DateOffset(months=10)
end_date = halving_date + DateOffset(months=10)

# Slice the DataFrame to get data for this cycle
cycle_data = btc_data.loc[start_date:end_date]

# Find low and high prices
low_price = cycle_data['Close'].min()
high_price = cycle_data['Close'].max()

# Calculate price as percentage of the range
cycle_data['Percentage'] = (cycle_data['Close'] - low_price) / (high_price - low_price) * 100

# Now cycle_data includes the price percentage for each day in the cycle range
