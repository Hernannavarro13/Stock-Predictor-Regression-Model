import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

# Download 5 years of stock data for a particular ticker
ticker = "NVDA"
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)
stock_data = yf.download(ticker, start=start_date, end=end_date)



def load_stock_data(ticker, start="2020-01-01"):
    df = yf.download(ticker, start=start)
    df = df[['Close', 'High', 'Low', 'Open', 'Volume']]
    return df


# Preview the data
print(stock_data.head())

