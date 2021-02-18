"""Simple ussage of public Kraken REST API"""
from datetime import datetime
import requests
import pandas as pd
import numpy as np
from scipy import signal
from scipy.signal import argrelextrema
import libs.krakenDict


def getData(pair: str) -> pd.DataFrame:
    """Return data from kraken  public api"""
    apiURL = "https://api.kraken.com/0/public/OHLC"
    payloads = libs.krakenDict.krakenDict[pair]["payloads"]
    data = requests.get(apiURL, params=payloads).json()
    df = pd.DataFrame.from_dict(
        data["result"][libs.krakenDict.krakenDict[pair]["result"]]
    )
    df[4] = df[4].astype(float)
    df.columns = [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "vwap",
        "volume",
        "count",
    ]
    df["datetime"] = [datetime.fromtimestamp(x) for x in df["timestamp"]]
    df["open"] = df["open"].astype(float)
    df["volume"] = df["volume"].astype(float)
    df["oc"] = df["open"] - df["close"]
    df["color"] = np.where(df["oc"] < 0, "red", "green")
    # apply filter to cloase filters
    filterB, filterA = signal.butter(3, 0.05)
    df["filter"] = signal.filtfilt(filterB, filterA, df["close"])

    DEPTH = 20
    df["min"] = df.iloc[
        argrelextrema(df["close"].values, np.less_equal, order=DEPTH)[0]
    ]["close"]
    df["max"] = df.iloc[
        argrelextrema(df["close"].values, np.greater_equal, order=DEPTH)[0]
    ]["close"]
    meanVol = df[df["volume"] > 0]["volume"].mean()
    df["maxvol"] = df.iloc[((df["volume"] > 3 * meanVol) & (df["oc"] > 0)).values][
        "close"
    ]
    return df
