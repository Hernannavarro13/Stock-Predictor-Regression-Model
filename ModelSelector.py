# ModelSelector.py

import yfinance as yf
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import DataCollector as stock
import Indicators

# Ensure you have ticker and historical data
ticker = "NVDA"  # Define the stock ticker
df = stock.load_stock_data(ticker)

# Feature Engineering
df = Indicators.create_features(df)

# Split into features and target variable
X = df.drop("Close", axis=1)  # Features (exclude 'Close' as it's the target)
y = df["Close"]  # Target variable

# Normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
train_size = int(len(X) * 0.8)
X_train, X_test = X_scaled[:train_size], X_scaled[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Train the model (Ridge regression in this case)
model = Ridge(alpha=1.0)
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Save the model and scaler
joblib.dump(model, 'best_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")

# Output the predictions
print(f"Predictions: {predictions[:5]}")  # Print the first 5 predictions



