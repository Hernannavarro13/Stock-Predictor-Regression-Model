import PredictionTarget as predictor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import Indicators as Indicators  # Ensure this is imported for feature creation

# Perform feature engineering (create features first)
predictor.X = Indicators.create_features(predictor.stock_data)  # Use the feature creation function from Indicators

# Ensure you're only using the correct 5 features (e.g., 'DayOfWeek', 'Month', 'Year', 'MA5', 'RSI')
X = predictor.X[['DayOfWeek', 'Month', 'Year', 'MA5', 'RSI']]  # Select only these 5 features
y = predictor.y

# Determine the split point (80% train, 20% test)
split_idx = int(len(X) * 0.65)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

# Scale the features using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save the scaler to a file
joblib.dump(scaler, 'scaler.pkl')

print("Scaler saved as 'scaler.pkl'.")

# Now you can proceed to use this scaler in other scripts like TomorrowsPredictor.py




