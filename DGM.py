#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import yfinance as yf

def ddm(current_dividend, growth_rate, discount_rate, years):
   
    intrinsic_value = 0
    for i in range(years):
        intrinsic_value += current_dividend / (1 + discount_rate) ** (i+1)
        current_dividend *= (1 + growth_rate)
    # calculate terminal value
    terminal_value = current_dividend / (discount_rate - growth_rate)
    intrinsic_value += terminal_value
    return intrinsic_value

# Fetch the current dividend information for a specific stock using yfinance
ticker = "AAPL"
stock_info = yf.Ticker(ticker).info

# Retrieve the current annual dividend per share
current_dividend = stock_info["regularCashDividend"]

# Assume a constant growth rate of dividends
growth_rate = 0.03

# Assume a required rate of return of 10%
discount_rate = 0.10

# Assume forecasting dividends for 10 years
years = 10

intrinsic_value = ddm(current_dividend, growth_rate, discount_rate, years)
print(intrinsic_value)

