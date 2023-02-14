#!/usr/bin/env python
# coding: utf-8
#Note: this program uses one year lagging data and the fcf percentage of revenue still needs to be added

# In[273]:

#GET YOUR API KEY FROM https://site.financialmodelingprep.com/developer/docs/#Revenue-Geographic-by-Segments 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from lxml import html
import matplotlib.pyplot as plt

#ticker input
company = "UNH"

#assumptions
rr = 0.13
multiple = 6
pgr = 0.025
cfgrowthrate = .07 #not exactly rev

url = (f"https://www.gurufocus.com/term/total_rvn_growth_5y_est/{company}/Total-Revenue-Growth-Rate-(Future-3Y-To-5Y-Est)/{company}")
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#driver.get(url)
page = requests.get(url)
tree = html.fromstring(page.content)
elements = tree.xpath('//*[@id="target_def_description"]/p[2]/strong[2]')
rpgr = elements[0].text


dummy = 1
api_key= ("api")
balancesheet = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?limit={dummy}&apikey={api_key}')
balancesheet = balancesheet.json()
cashAndShortTermInvestments = (balancesheet[0]['cashAndShortTermInvestments'])
totalDebt = (balancesheet[0]['totalDebt'])
netdebt = cashAndShortTermInvestments - totalDebt


incomestatement =  requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?limit={dummy}&apikey={api_key}')
incomestatement = incomestatement.json()
outstandingshares = incomestatement[0]['weightedAverageShsOutDil'] 

cashflow =  requests.get(f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{company}?limit={dummy}&apikey={api_key}')
cashflow = cashflow.json()
freecashflow = cashflow[0]['freeCashFlow']  #add in years so rate #automate

years= [1, 2, 3, 4, 5]
futurefreecashflow = []
discountfactor = []
discountedfuturefreecashflow = []
terminalvalue = freecashflow * (1+pgr)/(rr-pgr)

for year in years:
    cashflow = freecashflow *(1+cfgrowthrate)**year
    futurefreecashflow.append(cashflow)
    discountfactor.append((1+rr)**year)
for i in range(0, len(years)):
    discountedfuturefreecashflow.append(futurefreecashflow[i]/discountfactor[i])

ddnetdebt = (netdebt/(1+rr)**5)
mv = futurefreecashflow[-1] * multiple
mvd = mv/discountfactor[-1]
todaysvaluee = (mvd + ddnetdebt)/outstandingshares #last year growth not included (2021 info)
fvv = todaysvaluee 

discountedterminalvalue = terminalvalue/(1+rr)**5
discountedfuturefreecashflow.append(discountedterminalvalue)  
todaysvalue = sum(discountedfuturefreecashflow) 
fv = todaysvalue/outstandingshares  

dnetdebt = (netdebt/(1+rr)**5)/outstandingshares
fv_nd = dnetdebt + fv


print (f"Fair value is {fv}")
print (f"Fair value with net debt is {fv_nd}")
print (f"The future revenue growth rate is {rpgr}")
print (netdebt)
print(fvv)


# In[275]:



print(futurefreecashflow[2])


# In[ ]:




