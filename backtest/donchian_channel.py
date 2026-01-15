import pandas as pd
import numpy as np
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import warnings
warnings.filterwarnings("ignore")

# Load the filtered data (uses the dataset available in this repo)
data_path = '/Users/adjiitungin/Documents/Aji belajar/trade-rsch/backtest/data/BTC_30m_20260114_152420_historical.csv'
# The CSV is expected to have a 'timestamp' column
data = pd.read_csv(data_path, parse_dates=['timestamp'], index_col='timestamp')

# Ensure necessary columns are present and rename correctly
# Based on the CSV headers: datetime,open,high,low,close,volume,<extra>
data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
# Drop the unnecessary column
if 'Unnamed: 6' in data.columns:
    data.drop(columns=['Unnamed: 6'], inplace=True)

class DonchianChannelShort(Strategy):
    dc_period = 30
    atr_period = 30  # will be aligned to dc_period in init
    atr_ratio = 0.005  # ATR normalization ratio (0.3%–0.8% recommended)
    dc_width_threshold = 0.015  # adjusted threshold within 0.012–0.02
    risk_per_trade = 0.003  # reduced risk per trade (0.25%–0.35%)

    def init(self):
        # Donchian Channels: Upper = rolling max(High), Lower = rolling min(Low)
        self.dc_upper = self.I(lambda high, p: pd.Series(high).rolling(int(p)).max().values,
                               self.data.High, self.dc_period)
        self.dc_lower = self.I(lambda low, p: pd.Series(low).rolling(int(p)).min().values,
                               self.data.Low, self.dc_period)

        # ATR aligned with Donchian period; threshold uses ATR ratio vs price
        self.atr_period = self.dc_period
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period)

        # Donchian Channel width ratio: (upper - lower) / close
        self.dc_width = self.I(lambda: (self.dc_upper - self.dc_lower) / self.data.Close)

        # Track current stop loss to manage trailing
        self.current_sl = None

    # Disable long trades to enforce short-only testing
    def buy(self, *args, **kwargs):
        return

    def _is_trend_regime(self):
        """Determine if current candle is in TREND regime based on thresholds."""
        return (self.dc_width[-1] > self.dc_width_threshold) and (self.atr[-1] > self.data.Close[-1] * self.atr_ratio)

    def _position_size_for_short(self, entry_price, stop_loss):
        """Compute position size given risk per trade and stop distance.
        size = risk_cash / (stop_loss - entry_price)
        """
        stop_distance = float(stop_loss - entry_price)
        if stop_distance <= 0:
            return 0
        risk_cash = float(self.equity * self.risk_per_trade)
        size = risk_cash / stop_distance
        return max(0, size)

    def next(self):
        # Ensure we have enough data for indexing (need dc_period and at least 3 candles)
        if len(self.data) < max(self.dc_period, self.atr_period) + 3:
            return

        close = self.data.Close
        # Determine current regime
        is_trend = self._is_trend_regime()

        if not self.position:
            # Short entry condition per spec:
            # close < DC_lower(previous) AND close_previous >= DC_lower(two_candles_ago)
            cond_short_break = (close[-1] < self.dc_lower[-2]) and (close[-2] >= self.dc_lower[-3])

            if is_trend and cond_short_break:
                # Use default size handling consistent with bb_squeeze_adx.py
                stop_loss = float(self.dc_upper[-2])  # Initial SL at previous DC upper
                self.sell(sl=stop_loss)
                self.current_sl = stop_loss
        else:
            # Trailing stop: for short position, SL = MIN(current SL, DC_upper(current))
            new_sl = float(min(self.current_sl if self.current_sl is not None else np.inf,
                               self.dc_upper[-1]))
            if self.current_sl is None or new_sl < self.current_sl:
                try:
                    self.position.set_sl(new_sl)
                except Exception:
                    # Fallback in case set_sl isn't supported
                    pass
                self.current_sl = new_sl

            # Exit if price crosses trailing stop for short (close > stop_loss)
            if self.current_sl is not None and close[-1] > self.current_sl:
                self.position.close()
                self.current_sl = None
                return

            # Exit when regime switches to RANGE
            if not is_trend:
                self.position.close()
                self.current_sl = None

# Create and configure the backtest
bt = Backtest(data, DonchianChannelShort, cash=100000, commission=0.002)

# Run the backtest with default parameters and print the results
stats_default = bt.run()
print("Default Parameters Results:")
print(stats_default)

# Perform optimization over key parameters
optimization_results = bt.optimize(
    dc_period=range(30, 41, 5),
    dc_width_threshold=[0.012, 0.014, 0.016, 0.018, 0.02],
    atr_ratio=[0.003, 0.004, 0.005, 0.006, 0.008],
    risk_per_trade=[0.0025, 0.003, 0.0035],
    maximize='Equity Final [$]',
    constraint=lambda p: p.dc_period > 0 and p.dc_width_threshold > 0 and 0.0025 <= p.risk_per_trade <= 0.0035 and 0.003 <= p.atr_ratio <= 0.008,
)

# Print the optimization results and best parameters
print("Optimization Results:")
print(optimization_results)
print("Best Parameters:")
print("dc_period:", optimization_results._strategy.dc_period)
print("atr_period:", optimization_results._strategy.atr_period)
print("dc_width_threshold:", optimization_results._strategy.dc_width_threshold)
print("atr_ratio:", optimization_results._strategy.atr_ratio)
print("risk_per_trade:", optimization_results._strategy.risk_per_trade)