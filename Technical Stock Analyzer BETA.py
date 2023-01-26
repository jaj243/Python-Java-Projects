import pandas as pd
import ta

def calculate_rsi_macd_ma(df, period_rsi, fast_period, slow_period, signal_period, ma_period):
    # create the RSI indicator
    rsi = ta.momentum.RSIIndicator(close=df["close"], n=period_rsi)
    # add the RSI column to the dataframe
    df["RSI"] = rsi.rsi()
    # create the MACD indicator
    macd = ta.trend.MACD(close=df["close"], n_fast=fast_period, n_slow=slow_period, n_sign=signal_period)
    # add the MACD columns to the dataframe
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_diff"] = macd.macd_diff()
    #create the MA indicator
    df["ma"] = ta.trend.SMAIndicator(close=df["close"], n=ma_period).sma_indicator()
    return df

# load dataframe
df = pd.read_csv("stockdata.csv")
# calculate RSI with period 14 and MACD with fast_period=12, slow_period=26, signal_period=9 and 200-day MA
df = calculate_rsi_macd_ma(df, 14, 12, 26, 9, 200)
print(df)
