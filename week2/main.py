# region imports
from AlgorithmImports import *
# endregion

class BuildProject_Week2(QCAlgorithm):
    def initialize(self):
        self.set_start_date(2020, 1, 1) # Without a specified end date, it backtests from the beginning (90s)
        self.set_end_date(2025, 10, 16) # Without a specified end date, it backtests to present
        self.set_cash(1_000_000)
        
        self._symbol = self.add_equity("SPY", Resolution.DAILY).symbol
        #Changed to Shorter SMA = more sensitive to price changes, more trades.
        self._sma = self.sma(self._symbol, 20) # technical indicator (TI)
        self.last_action = None

        # Warmup changed to adjust SMA change
        self.set_warm_up(25)

    def on_data(self, data):
        # Ensure we have enough data to calculate the moving average
        if not self._sma.is_ready:
            self.log("SMA is not ready!")
            return
        
        if self._symbol not in data or data[self._symbol] is None:
            self.log("Data not available for SPY")
            return
        
        price = data[self._symbol].close

        # Buy if the price is above the moving average
        if price > self._sma.current.value:
            if not self.portfolio.invested or self.last_action == "Sell":
                self.set_holdings(self._symbol, 1) # buy. 1 = 100%, 0.5 = 50%. -1 = short!
                self.last_action = "Buy"
                self.log("Price > SMA :: Entering the Market")

        # Sell if the price is below the moving average
        elif price < self._sma.current.value:
            if self.portfolio.invested and self.last_action == "Buy":
                self.liquidate(self._symbol) # sell
                self.last_action = "Sell"
                self.log("Price < SMA :: Exiting the Market")
