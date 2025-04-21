import yfinance as yf
import Indicators  # Assuming you have your feature engineering functions here
import joblib
from sklearn.preprocessing import StandardScaler
import json

def get_data(ticker):
    # Fetch more data (e.g., last 100 days instead of just 7)
    df = yf.download(ticker, period="100d", auto_adjust=True)
    
    # Ensure there's enough data before applying feature engineering
    if df.shape[0] < 50:
        raise ValueError("Not enough data to apply feature engineering. Consider using more historical data.")
    
    print(f"Data before feature engineering: {df.shape}")  # Optional debug line
    
    df = Indicators.create_features(df)  # Apply feature engineering
    
    print(f"Data after feature engineering: {df.shape}")  # Optional debug line
    
    df = df.dropna()  # Drop any missing values
    return df

def predict_next_day(ticker):
    df = get_data(ticker)
    
    # Load the best model (this assumes you have saved your model previously)
    model = joblib.load('best_model.pkl')
    
    # Ensure you are passing the correct features that the model expects
    # Only select the features used during training
    features = df[['DayOfWeek', 'Month', 'Year', 'MA5', 'RSI']]  # Select only 5 features, not 6
    
    # Load the scaler used during training
    scaler = joblib.load('scaler.pkl')
    
    # Load feature columns
    with open('feature_columns.json', 'r') as f:
        expected_columns = json.load(f)

    # Align the features with the expected order
    features = features[expected_columns]
    features_scaled = scaler.transform(features)

    # Make prediction
    prediction = model.predict(features_scaled)[0]
    
    return prediction

if __name__ == "__main__":
    ticker = "NVDA"  # Example ticker, change as needed
    next_price = predict_next_day(ticker)
    print(f"The predicted price for {ticker} tomorrow is: {next_price}")









