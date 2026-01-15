import pandas as pd
import numpy as np
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import warnings
warnings.filterwarnings("ignore")

# Load the filtered data (use local project data path)
data_path = '/Users/adjiitungin/Documents/Aji belajar/trade-rsch/backtest/data/BTC_30m_20260114_152420_historical.csv'
data = pd.read_csv(data_path, parse_dates=['timestamp'], index_col='timestamp')

# Ensure necessary columns are present and rename correctly
# Expected columns order: Open, High, Low, Close, Volume, Extra
data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
# Drop the unnecessary column
if 'Unnamed: 6' in data.columns:
    data.drop(columns=['Unnamed: 6'], inplace=True)

class MSBOrderBlockStrategy(Strategy):
    zigzag_len = 9
    fib_factor = 0.33

    def init(self):
        # State for MSB pivots and market regime
        self.trend = 1  # 1 = up, -1 = down
        self.market = 1  # 1 = bull, -1 = bear
        self.high_points = []
        self.low_points = []
        # Last detected OB zones (top/bottom)
        self.bu_ob_top = None
        self.bu_ob_bot = None
        self.be_ob_top = None
        self.be_ob_bot = None

    def _highest_recent(self, n):
        return max(self.data.High[-i] for i in range(1, n + 1))

    def _lowest_recent(self, n):
        return min(self.data.Low[-i] for i in range(1, n + 1))

    def _recent_min_info(self, n):
        vals = [self.data.Low[-i] for i in range(1, n + 1)]
        idx = int(np.argmin(vals))  # 0 = most recent bar
        return vals[idx], idx + 1  # lookback distance

    def _recent_max_info(self, n):
        vals = [self.data.High[-i] for i in range(1, n + 1)]
        idx = int(np.argmax(vals))
        return vals[idx], idx + 1

    def _update_pivots_on_trend_change(self, to_up, to_down):
        changed = False
        if self.trend == -1 and to_up:
            self.trend = 1
            low_val, _ = self._recent_min_info(self.zigzag_len)
            self.low_points.append(low_val)
            changed = True
        elif self.trend == 1 and to_down:
            self.trend = -1
            high_val, _ = self._recent_max_info(self.zigzag_len)
            self.high_points.append(high_val)
            changed = True
        return changed

    def _update_market_regime(self):
        if len(self.high_points) >= 2 and len(self.low_points) >= 2:
            h0, h1 = self.high_points[-1], self.high_points[-2]
            l0, l1 = self.low_points[-1], self.low_points[-2]
            prev_market = self.market
            if self.market == 1 and l0 < l1 and l0 < (l1 - abs(h0 - l1) * self.fib_factor):
                self.market = -1
            elif self.market == -1 and h0 > h1 and h0 > (h1 + abs(h1 - l0) * self.fib_factor):
                self.market = 1
            return prev_market != self.market
        return False

    def _find_last_bearish_candle_ob(self, lookback):
        # Find most recent bearish candle in last N bars -> OB from that candle's high/low
        for i in range(1, lookback + 1):
            if self.data.Open[-i] > self.data.Close[-i]:
                return self.data.High[-i], self.data.Low[-i]
        return None, None

    def _find_last_bullish_candle_ob(self, lookback):
        # Find most recent bullish candle in last N bars -> OB from that candle's high/low
        for i in range(1, lookback + 1):
            if self.data.Open[-i] < self.data.Close[-i]:
                return self.data.High[-i], self.data.Low[-i]
        return None, None

    def next(self):
        if len(self.data) < max(self.zigzag_len, 20):
            return

        # Zigzag logic to detect trend toggles similar to Pinescript
        to_up = self.data.High[-1] >= self._highest_recent(self.zigzag_len)
        to_down = self.data.Low[-1] <= self._lowest_recent(self.zigzag_len)

        # Update pivots when trend changes
        trend_changed = self._update_pivots_on_trend_change(to_up, to_down)

        # Update market regime based on last pivots (MSB)
        market_changed = self._update_market_regime()

        # On market change, update Order Blocks as in script
        if market_changed:
            if self.market == 1:
                # Bullish market -> detect Buy OB from last bearish candle
                top, bot = self._find_last_bearish_candle_ob(self.zigzag_len)
                if top is not None:
                    self.bu_ob_top, self.bu_ob_bot = top, bot
            else:
                # Bearish market -> detect Sell OB from last bullish candle
                top, bot = self._find_last_bullish_candle_ob(self.zigzag_len)
                if top is not None:
                    self.be_ob_top, self.be_ob_bot = top, bot

        # Trading logic mirrors Pinescript: enter when price is inside OB, SL at OB edge, TP at nearest opposite OB
        close = self.data.Close[-1]
        if not self.position:
            # LONG setup
            if self.market == 1 and self.bu_ob_top and self.bu_ob_bot and self.be_ob_top and self.be_ob_bot:
                if self.bu_ob_bot < close < self.bu_ob_top:
                    sl = self.bu_ob_bot
                    tp = self.be_ob_bot
                    # Ensure broker constraints: SL < entry < TP
                    if sl < close and tp > close:
                        self.buy(sl=sl, tp=tp)
            # SHORT setup
            elif self.market == -1 and self.be_ob_top and self.be_ob_bot and self.bu_ob_top and self.bu_ob_bot:
                if self.be_ob_bot < close < self.be_ob_top:
                    sl = self.be_ob_top
                    # Prefer bu_ob_top for TP, but must be below entry for shorts
                    tp = self.bu_ob_top
                    if tp is None or tp >= close:
                        # Fallback to bu_ob_bot if it satisfies short TP constraint
                        tp = self.bu_ob_bot
                    # Ensure broker constraints: TP < entry < SL
                    if tp is not None and tp < close and sl > close:
                        self.sell(sl=sl, tp=tp)

# Create and configure the backtest
bt = Backtest(data, MSBOrderBlockStrategy, cash=100000, commission=0.002)

# Run the backtest with default parameters and print the results
stats_default = bt.run()
print("Default Parameters Results:")
print(stats_default)

# Optimization over core parameters
optimization_results = bt.optimize(
    zigzag_len=range(5, 20, 2),
    fib_factor=[round(i, 2) for i in np.arange(0.1, 0.6, 0.05)],
    maximize='Equity Final [$]',
    constraint=lambda p: p.zigzag_len > 1 and 0 < p.fib_factor < 1
)

print(optimization_results)
print("Best Parameters:")
print("ZigZag Length:", optimization_results._strategy.zigzag_len)
print("Fib Factor:", optimization_results._strategy.fib_factor)