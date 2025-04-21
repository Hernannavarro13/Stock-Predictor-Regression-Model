import pandas as pd
import numpy as np
import yfinance as yf
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import Indicators  # Assuming your feature creation code is here
import DataCollector as stock  # Assuming this is where your stock data is collected

# Step 1: Data collection
def get_data(ticker):
    # Fetching the last 200 days of data
    end_date = pd.to_datetime('today')
    start_date = end_date - pd.DateOffset(days=200)  # Collect 200 days of stock data
    
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
    
    if data.empty:
        raise ValueError(f"Failed to fetch data for {ticker}.")
    
    return data

# Step 2: Feature engineering using Indicators
def prepare_data(df):
    # Create features using the Indicators module
    print("Data shape before feature engineering:", df.shape)
    df = Indicators.add_technical_indicators(df)
    print("Data shape after feature engineering:", df.shape)
    
    # Ensure there are no NaN values
    df = df.dropna()
    
    return df

# Step 3: Split data into features and target
def split_data(df):
    # Now using all 12 features
    X = df[['DayOfWeek', 'Month', 'Year', 
            'MA5', 'MA10', 'MA20',  # 3 moving averages
            'RSI', 'MACD',           # RSI and MACD
            'Bollinger_Band_Upper', 'Bollinger_Band_Lower',  # Bollinger Bands
            'Momentum', 'Volume_Change']]  # Momentum and volume change
    
    y = df['Close']  # Predicting Close price
    
    return X, y


# Step 4: Train the model
def train_model(X, y):
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # Scale the data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train a linear regression model
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    
    # Save the model and scaler
    joblib.dump(model, 'best_model.pkl')  # Saving the trained model
    joblib.dump(scaler, 'scaler.pkl')  # Saving the scaler
    
    print("Model training complete. Model and scaler saved.")
    
    # Save the feature column order
    import json
    with open('feature_columns.json', 'w') as f:
        json.dump(list(X.columns), f)

    return model, scaler

# Step 5: Main function to execute the script
def main():
    # Get the stock data
    ticker = stock.ticker  # Assuming this is the ticker you're working with
    df = get_data(ticker)
    
    # Prepare the data (feature engineering)
    df = prepare_data(df)
    
    # Split the data
    X, y = split_data(df)
    
    # Train and save the model
    model, scaler = train_model(X, y)

# Run the script
if __name__ == "__main__":
    main()
