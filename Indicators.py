import ta

def add_technical_indicators(df):
    # Ensure 'Close' column is passed as a 1D Series
    close = df['Close']  # 1D Series, not df[['Close']]
    
    # RSI
    rsi = ta.momentum.RSIIndicator(close=close).rsi()
    df['RSI'] = rsi

    # Moving Averages
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA10'] = df['Close'].rolling(window=10).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(close=close)
    df['Bollinger_Band_Upper'] = bb.bollinger_hband()
    df['Bollinger_Band_Lower'] = bb.bollinger_lband()

    # Momentum - using Stochastic Oscillator
    df['Momentum'] = ta.momentum.StochasticOscillator(
        high=df['High'], low=df['Low'], close=close
    ).stoch()

    # Volume change percentage
    df['Volume_Change'] = df['Volume'].pct_change()

    # Date features
    df['DayOfWeek'] = df.index.dayofweek
    df['Month'] = df.index.month
    df['Year'] = df.index.year

    # Drop NaN values introduced by indicators
    df = df.dropna()

    return df










