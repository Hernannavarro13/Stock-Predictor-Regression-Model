import pandas as pd

def create_features(df):
    # Check if 'Close' and 'Volume' columns exist
    if 'Close' not in df.columns or 'Volume' not in df.columns:
        raise ValueError("The input dataframe must contain 'Close' and 'Volume' columns.")

    # Create date features
    df['DayOfWeek'] = df.index.dayofweek
    df['Month'] = df.index.month
    df['Year'] = df.index.year
    
    # Create basic technical indicators
    df['MA5'] = df['Close'].rolling(window=5).mean()  # Moving Average
    df['RSI'] = df['Close'].diff().where(df['Close'].diff() > 0, 0).rolling(window=7).mean()  # RSI with a shorter window
    df['Volume_Change'] = df['Volume'].pct_change()  # Percentage change in volume
    
    # Drop NaN values generated during feature calculation
    df = df.dropna()

    # Ensure there is enough data after dropping NaNs (adjust threshold if needed)
    if df.shape[0] < 50:  # Minimum threshold of 50 rows
        raise ValueError("Not enough data after feature engineering. Consider using more historical data.")

    return df

