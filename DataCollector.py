import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

# Download 5 years of stock data for a particular ticker
ticker = "AAPL"
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)
stock_data = yf.download(ticker, start=start_date, end=end_date)

# Preview the data
print(stock_data.head())