# In BackTestStrat.py

import ModelSelector as ms
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the stock data using the method from ModelSelector
df = ms.load_data("NVDA")  # Replace 'NVDA' with any stock ticker

# Now you can load the best model and predictions
best_model_name, best_model, best_predictions, X_test, y_test, y_scaler = ms.get_best_model()

# Check lengths of the predictions and X_test
print(f"Length of X_test: {len(X_test)}")
print(f"Length of best_predictions: {len(best_predictions)}")
print(f"Length of df: {len(df)}")

# Ensure predictions align with the correct subset of df
df.loc[X_test.index, 'Predicted_Close'] = best_predictions

# Add a 'Signal' column based on the prediction
df['Signal'] = 0  # Default to no action
df.loc[df['Predicted_Close'].shift(1) > df['Close'].shift(1), 'Signal'] = 1  # Buy signal

# Calculate strategy performance
df['Strategy'] = df['Signal'] * df['Close'].pct_change()  # Percent change based on signals
df['Cumulative_Strategy'] = (1 + df['Strategy']).cumprod()  # Cumulative strategy returns

# Plot the performance
plt.figure(figsize=(12, 6))

# Plot actual close prices
plt.plot(df.index, df['Close'], label='Actual Price', color='blue')

# Plot predicted close prices
plt.plot(df.index, df['Predicted_Close'], label='Predicted Price', linestyle='--', color='orange')

# Plot cumulative strategy returns
plt.plot(df.index, df['Cumulative_Strategy'], label='Cumulative Strategy', linestyle='-.', color='green')

# Adding labels and title
plt.title('Stock Price Prediction and Strategy Performance')
plt.xlabel('Date')
plt.ylabel('Price / Return')
plt.legend(loc='best')

# Show the plot
plt.show()





