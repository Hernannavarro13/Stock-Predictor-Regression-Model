import yfinance as yf
import Indicators
import joblib
from sklearn.preprocessing import StandardScaler
import json

def get_data(ticker):
    df = yf.download(ticker, period="100d", auto_adjust=True)

    if df.shape[0] < 50:
        raise ValueError("Not enough data to apply feature engineering.")

    print(f"Data before feature engineering: {df.shape}")
    df = Indicators.add_technical_indicators(df)
    print(f"Data after feature engineering: {df.shape}")

    df = df.dropna()
    return df

def predict_next_day(ticker):
    df = get_data(ticker)

    # Load trained model and scaler
    model = joblib.load('best_model.pkl')
    scaler = joblib.load('scaler.pkl')

    # Load the saved feature column order
    with open('feature_columns.json', 'r') as f:
        expected_columns = json.load(f)

    # Select and scale features
    features = df[expected_columns]
    features_scaled = scaler.transform(features)

    # Predict next day's price (take last row)
    prediction = model.predict(features_scaled)[-1]
    return prediction

if __name__ == "__main__":
    ticker = "NVDA"
    next_price = predict_next_day(ticker)
    print(f"The predicted price for {ticker} tomorrow is: {next_price}")


