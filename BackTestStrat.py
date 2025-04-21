import ModelSelector as Model
import numpy as np
import pandas as pd
import TrainTestSplit as Train
import DataCollector as stock


def backtest_strategy(data, predictions, investment=10000):
    # Reset index to ensure alignment
    backtest_data = data.reset_index(drop=True).copy()
    predictions = pd.Series(predictions).reset_index(drop=True)

    # Check shape
    if len(backtest_data) != len(predictions):
        raise ValueError(f"Shape mismatch: data={len(backtest_data)}, predictions={len(predictions)}")

    # Use correct MultiIndex reference
    close_col = ('Close', stock.ticker)
    pred_col = ('Predicted_Close', '')  # Match MultiIndex structure

    # Add prediction column as part of MultiIndex
    backtest_data[pred_col] = predictions.values

    # Drop NaNs separately
    backtest_data = backtest_data.dropna(subset=[close_col])
    backtest_data = backtest_data.dropna(subset=[pred_col])

    # Strategy logic
    backtest_data[('Position', '')] = np.where(
        backtest_data[pred_col] > backtest_data[close_col], 1, -1)

    backtest_data[('Daily_Return', '')] = backtest_data[close_col].pct_change()
    backtest_data[('Strategy_Return', '')] = (
        backtest_data[('Position', '')].shift(1) * backtest_data[('Daily_Return', '')]
    )

    backtest_data[('Cumulative_Market_Return', '')] = (
        (1 + backtest_data[('Daily_Return', '')]).cumprod()
    )
    backtest_data[('Cumulative_Strategy_Return', '')] = (
        (1 + backtest_data[('Strategy_Return', '')]).cumprod()
    )

    # Final portfolio values
    market_final = investment * backtest_data[('Cumulative_Market_Return', '')].iloc[-1]
    strategy_final = investment * backtest_data[('Cumulative_Strategy_Return', '')].iloc[-1]

    print(f"Initial investment: ${investment}")
    print(f"Final market value: ${market_final:.2f}")
    print(f"Final strategy value: ${strategy_final:.2f}")
    print(f"Strategy outperformance: {(strategy_final / market_final - 1) * 100:.2f}%")

    return backtest_data


# Load predictions from best model
best_predictions = Model.results["Ridge Regression"]["predictions"]

# Slice stock data to match prediction length
backtest_df = stock.stock_data.iloc[Train.split_idx:].copy()
backtest_df = backtest_df.reset_index(drop=True).iloc[:len(best_predictions)]

# Run strategy backtest
backtest_results = backtest_strategy(backtest_df, best_predictions)

