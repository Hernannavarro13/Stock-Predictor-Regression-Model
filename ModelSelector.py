# In ModelSelector.py

import yfinance as yf
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

# Function to load stock data using yfinance
def load_data(ticker):
    """
    Function to load stock data using yfinance for a given ticker.
    """
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")  # Adjust the period as needed (e.g., '1d', '1mo', '1y', etc.)
    
    # Optional: Perform any preprocessing steps here (e.g., adding technical indicators)
    # Example: df = add_technical_indicators(df)
    
    return df

# Function to evaluate models and get predictions
def evaluate_model(model, X_train, X_test, y_train, y_test):
    # Align X and y to ensure they have the same number of rows
    X_train, y_train = X_train.align(y_train, join='inner', axis=0)
    X_test, y_test = X_test.align(y_test, join='inner', axis=0)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    predictions = model.predict(X_test)
    
    # Calculate Mean Squared Error
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")
    
    return model, predictions

# Function to get the best model (for example purposes)
def get_best_model():
    # Load stock data
    df = load_data("NVDA")
    
    # Example of setting up X and y (can be customized)
    X = df[['Open', 'High', 'Low', 'Volume']]  # Assuming these features
    y = df['Close']  # Target variable
    
    # Split data into train and test
    train_size = int(len(df) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    # Example: Train a Ridge Regression model
    model = Ridge()
    
    # Evaluate the model
    trained_model, predictions = evaluate_model(model, X_train, X_test, y_train, y_test)
    
    return "Ridge Regression", trained_model, predictions, X_test, y_test, None





