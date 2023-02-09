import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cvxpy as cp
import pypfopt
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from scipy.optimize import minimize
# Define the stock symbols you want to extract
symbols = ['C', 'GOOG', 'RHHBY', 'AVGO ', 'PYPL', 'ABNB','MU','AXP','BCS','ALL','Gild','INTC','DFS','SHEL','HSBC','DVA','AMKBY','HRB','WLKP','CVS','JEPI','SOXX','GLD']
#weights = np.array(['0.04', '0.04', '0.04', '0.04 ', '0.04', '0.04','0.04','0.04','0.04','0.04','0.04','0.04','0.04','0.04','0.04','0.04','0.04','0.04','0.04','0.04','0.04','0.04','0.04'])
# Define the start and end dates for the data
start_date = '2018-01-01'
end_date = '2022-12-31'

# Loop through the symbols and extract the close price data using yfinance
for symbol in symbols:
    data = yf.download(symbol, start=start_date, end=end_date)['Close']
    data.name = symbol
    if symbol == symbols[0]:
        df = (data / data.shift(1) - 1).to_frame()
    else:
        df[symbol] = (data / data.shift(1) - 1)

# Remove any rows containing NaN values
df = df.dropna()

# Plot the returns
df.plot(figsize=(20, 12))
plt.xlabel('Date')
plt.ylabel('Return')
plt.title('Stock Returns')
plt.show()

# Compute the average returns, variance, and standard deviation for each stock
average_returns = df.mean()
variance = df.var()
standard_deviation = df.std()

# Compute the correlation matrix
correlation_matrix = df.corr()

# Compute the covariance matrix
covariance_matrix = df.cov()

# Show the results
print("Correlation Matrix:")
print(correlation_matrix)
print("Covariance Matrix:")
print(covariance_matrix)

# Show the results
print("Average Returns:")
print(average_returns)
print("Variance:")
print(variance)
print("Standard Deviation:")
print(standard_deviation)
print(df)

# Show the heatmap of the correlation + covariance matrix
sns.heatmap(correlation_matrix, annot=True)
plt.title('Correlation Matrix Heatmap')
plt.show()

sns.heatmap(covariance_matrix, annot=True)
plt.title('Covariance Matrix Heatmap')
plt.show()


# Compute the expected returns and covariance matrix
#returns = df.mean()
#cov_matrix = df.cov()
#num_portfolios = 5000
#results = np.zeros((3,num_portfolios))
#weights_record = []

#for i in range(num_portfolios):
  #  weights = np.random.random(len(symbols))
 #   weights /= np.sum(weights)
   # weights_record.append(weights)
   # portfolio_return = np.sum(returns * weights) * 252
   # portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
  #  results[0,i] = portfolio_return
  #  results[1,i] = portfolio_volatility
  #  results[2,i] = results[0,i] / results[1,i]

# Plot the efficient frontier
#plt.figure(figsize=(10, 6))
#plt.scatter(results[1,:], results[0,:], c=results[2,:], cmap='YlGnBu', marker='o', s=10, alpha=0.3)
#plt.colorbar()
#plt.scatter(np.sqrt(np.diag(cov_matrix)), returns, marker='X', color='red', s=100, label='Individual Stocks')
#plt.xlabel('Volatility')
#plt.ylabel('Returns')
#plt.title('Efficient Frontier')
#plt.legend(labelspacing=0.8)
#plt.show()  

# Compute the expected returns and covariance matrix
returns = df.mean()
cov_matrix = df.cov()

# Define the objective function to minimize
def portfolio_volatility(weights, returns, cov_matrix):
    portfolio_return = np.sum(returns * weights) * 252
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return portfolio_volatility

def neg_sharpe_ratio(weights, returns, cov_matrix, risk_free_rate=0.01):
    portfolio_return = np.sum(returns * weights) * 252
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    return -sharpe_ratio

# Constraints and bounds
num_assets = len(symbols)
bounds = [(0,1) for i in range(num_assets)]
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

# Initial guess
init_guess = [1/num_assets for i in range(num_assets)]

# Optimize the portfolio for the Sharpe ratio
results = minimize(fun=neg_sharpe_ratio, x0=init_guess, args=(returns, cov_matrix), method='SLSQP', bounds=bounds, constraints=constraints)
weights = results['x']

# Display the optimized weights and Sharpe ratio
print(weights)
print('Sharpe ratio:', -results['fun'])
# Generate the efficient frontier
portfolio_returns = []
portfolio_volatilities = []
risk_free_rate = 0.01

for x in range(100):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    portfolio_return = np.sum(returns * weights) * 252
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    portfolio_returns.append(portfolio_return)
    portfolio_volatilities.append(portfolio_volatility)

# Plot the efficient frontier
plt.figure(figsize=(10, 8))
sharpe_ratios = [ret / vol for ret, vol in zip(portfolio_returns, portfolio_volatilities)]
plt.scatter(portfolio_volatilities, portfolio_returns, c=sharpe_ratios, marker='o')
plt.plot(portfolio_volatilities, portfolio_returns, 'y-o')
plt.xlabel('Expected Volatility')
plt.ylabel('Expected Return')
plt.colorbar(label='Sharpe Ratio')
plt.show()
