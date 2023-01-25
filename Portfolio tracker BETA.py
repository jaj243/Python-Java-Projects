#!/usr/bin/env python
# coding: utf-8

# In[7]:


import yfinance as yf
import matplotlib.pyplot as plt

class PortfolioTracker:
    def __init__(self):
        self.portfolio = pd.DataFrame(columns=["Ticker", "Shares", "Price", "Dividend","Beta"])
    
    def add_stock(self, ticker, shares):
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        self.portfolio = self.portfolio.append({"Ticker": ticker, "Shares": shares, "Price": stock_info["regularMarketPrice"], "Dividend": stock_info["regularMarketDividend"], "Beta": stock_info["beta"]}, ignore_index=True)
    
    def remove_stock(self, ticker):
        self.portfolio = self.portfolio[self.portfolio.Ticker != ticker]
    
    def update_stock_price(self, ticker):
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        self.portfolio.loc[self.portfolio.Ticker == ticker, "Price"] = stock_info["regularMarketPrice"]
        self.portfolio.loc[self.portfolio.Ticker == ticker, "Dividend"] = stock_info["regularMarketDividend"]
        self.portfolio.loc[self.portfolio.Ticker == ticker, "Beta"] = stock_info["beta"]
    def current_value(self):
        return self.portfolio["Shares"].mul(self.portfolio["Price"]).sum()

    def total_dividend(self):
        return self.portfolio["Shares"].mul(self.portfolio["Dividend"]).sum()

    def portfolio_beta(self):
        beta_weighted = self.portfolio["Shares"] * self.portfolio["Beta"]
        total_shares = self.portfolio["Shares"].sum()
        return beta_weighted.sum() / total_shares

    def print_portfolio(self):
        print(self.portfolio)
        
    def plot_portfolio(self):
        self.portfolio.plot(kind='bar', x='Ticker', y=['Shares', 'Price', 'Dividend'])
        plt.show()


# In[ ]:




