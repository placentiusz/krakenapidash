"""Module for data analyse"""
from enum import Enum
import pandas as pd


class Status(Enum):
    """Status for analyse"""

    BUY = 1
    SELL = -1
    STAY = 0


class Signals:
    """Signals for buy and sell"""

    def __init__(self, dataframe: pd.DataFrame):
        self.analizedDataFrame = dataframe

    def dataAnalize(self) -> int:
        """Main method for analyse"""
        raise NotImplementedError("Not implemented")


class StatusSimpleMinMax(Signals):
    """Simple mix and max"""

    def dataAnalize(self) -> Status:
        last = self.analizedDataFrame["close"].iloc[-1]
        minClose = self.analizedDataFrame["close"].quantile(0.10)
        maxClose = self.analizedDataFrame["close"].quantile(0.90)
        print(minClose, maxClose)
        if last < minClose:
            return Status.BUY
        if last > maxClose:
            return Status.SELL

        return Status.STAY
