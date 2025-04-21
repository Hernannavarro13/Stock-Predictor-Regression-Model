import yfinance as yf
from datetime import datetime, timedelta

# Define default ticker (used in training script)
ticker = "NVDA"

def get_historical_data(ticker=ticker, years=5):
    """
    Downloads stock data for the past `years` for the specified ticker.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
    return df

def load_stock_data(ticker, start="2020-01-01"):
    """
    Loads historical data from a given start date with only essential columns.
    """
    df = yf.download(ticker, start=start, auto_adjust=True)
    return df[['Close', 'High', 'Low', 'Open', 'Volume']]

# Debug print if you want to preview data
if __name__ == "__main__":
    df = get_historical_data()
    print(df.head())


