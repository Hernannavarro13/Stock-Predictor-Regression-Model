import matplotlib.pyplot as plt
import seaborn as sns
import BackTestStrat as bt
import DataCollector as stock

# Set style
sns.set_theme(style='whitegrid')

# Plot actual vs. predicted prices
plt.figure(figsize=(12, 6))
plt.plot(bt.backtest_df.index, bt.backtest_df['Close'], label='Actual Price')
plt.plot(bt.backtest_df.index, bt.best_predictions, label='Predicted Price', alpha=0.7)
plt.title(f'{stock.ticker} - Actual vs Predicted Prices')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.legend()
plt.tight_layout()
plt.show()

# Plot strategy performance
plt.figure(figsize=(12, 6))
plt.plot(bt.backtest_results.index, bt.backtest_results['Cumulative_Market_Return'], label='Buy and Hold')
plt.plot(bt.backtest_results.index, bt.backtest_results['Cumulative_Strategy_Return'], label='Model Strategy')
plt.title(f'{stock.ticker} - Strategy Performance')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.tight_layout()
plt.show()