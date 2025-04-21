import DataCollector as datacollector
def create_features(df):
    # Create date features
    df['DayOfWeek'] = df.index.dayofweek
    df['Month'] = df.index.month
    df['Year'] = df.index.year
    
    # Create technical indicators
    # Moving averages
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    
    # Relative Strength Index (simplified)
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    
    # Volatility
    df['Volatility'] = df['Close'].rolling(window=20).std()
    
    # Price momentum
    df['Price_momentum'] = df['Close'] / df['Close'].shift(10) - 1
    
    # Trading volume features
    df['Volume_Change'] = df['Volume'].pct_change()
    df['Volume_MA5'] = df['Volume'].rolling(window=5).mean()
    
    # Drop NaN values
    df = df.dropna()
    
    return df

# Apply feature engineering
stock_data = create_features(datacollector.stock_data)