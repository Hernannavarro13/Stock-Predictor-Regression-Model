import DataCollector as stock
# Create target variable - next day's closing price
stock.stock_data.loc[:, 'Target'] = stock.stock_data['Close'].shift(-1)

# Remove the last row since it won't have a target
stock_data = stock.stock_data.dropna()

# Split features and target
X = stock_data.drop(['Target'], axis=1)
y = stock_data['Target']