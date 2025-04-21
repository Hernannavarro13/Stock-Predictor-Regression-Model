import PredictionTarget as predictor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Determine the split point (80% train, 20% test)
split_idx = int(len(predictor.X) * 0.65)
X_train, X_test = predictor.X.iloc[:split_idx], predictor.X.iloc[split_idx:]
y_train, y_test = predictor.y.iloc[:split_idx], predictor.y.iloc[split_idx:]

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)