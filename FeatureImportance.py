import joblib
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import ModelSelector as selector  # Assuming this is where models are trained
import Indicators as Indicators

# Function to train and save the model
def train_and_save_best_model():
    # Assuming your model selection and training code is in the ModelSelector module
    best_model_name = "Ridge Regression"  # Example, update with your best model selection
    best_model = selector.models[best_model_name]  # Load the model from ModelSelector
    
    # Save the best model
    joblib.dump(best_model, 'best_model.pkl')
    print("Best model saved as 'best_model.pkl'")

# If you haven't run this yet, uncomment this line to train and save the model
# train_and_save_best_model()

# The rest of the code remains the same
def create_features(df):
    # Check if 'Close' and 'Volume' columns exist
    if 'Close' not in df.columns or 'Volume' not in df.columns:
        raise ValueError("The input dataframe must contain 'Close' and 'Volume' columns.")

    # Create date features (will use only 5 features for training)
    df['DayOfWeek'] = df.index.dayofweek
    df['Month'] = df.index.month
    df['Year'] = df.index.year
    
    # Create only the basic technical indicators used for training
    df['MA5'] = df['Close'].rolling(window=5).mean()  # Moving Average
    df['RSI'] = df['Close'].diff().where(df['Close'].diff() > 0, 0).rolling(window=7).mean()  # RSI with a shorter window
    df['Volume_Change'] = df['Volume'].pct_change()  # Percentage change in volume
    
    # Drop NaN values generated during feature calculation
    df = df.dropna()

    # Ensure there is enough data after dropping NaNs
    if df.shape[0] < 50:  # Minimum threshold of 50 rows
        raise ValueError("Not enough data after feature engineering. Consider using more historical data.")

    return df


