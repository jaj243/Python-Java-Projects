import schedule
import time
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Define a list of tickers
tickers = ["AAPL", "GOOG", "MSFT", "IBM", "AMZN"]

# Define the start and end dates for the historical data
start_date = "2010-01-01"
end_date = "2022-12-31"

# Define the frequency of the data
frequency = "1d"  # daily

# Get the stock data for all tickers
stock_data = {}
for ticker in tickers:
    stock_data[ticker] = yf.download(ticker, start=start_date, end=end_date, interval=frequency)

# Create a DataFrame with the closing prices of all stocks
closing_prices = pd.DataFrame({ticker: data["Close"] for ticker, data in stock_data.items()})

# Calculate the correlation matrix
correlation_matrix = closing_prices.corr()

# Plot the stock prices over time
plt.figure(figsize=(10,5))
for ticker, data in stock_data.items():
    data["Close"].plot(label=ticker)

# Add labels and legend
plt.xlabel("Date")
plt.ylabel("Closing Price")
plt.legend()
plt.title("Stock Prices over Time")

# Create another figure for the correlation matrix
plt.figure(figsize=(5,5))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Stock Correlation")
ols_result = sm.OLS(closing_prices.iloc[:, 0], closing_prices.iloc[:, 1:]).fit()
print(ols_result.summary())

plt.show()



#for live updating
#def job():
 #   stock_data = {}
  #  for ticker in tickers:
   #     stock_data[ticker] = yf.download(ticker)
    # your plotting code here

#schedule.every(10).minutes.do(job)

#while True:
 #   schedule.run_pending()
  #  time.sleep(1)
