import Indicators as indicate
# Create target variable - next day's closing price
indicate.stock_data.loc[:, 'Target'] = indicate.stock_data['Close'].shift(-1)

# Remove the last row since it won't have a target
stock_data = indicate.stock_data.dropna()

# Split features and target
X = stock_data.drop(['Target'], axis=1)
y = stock_data['Target']