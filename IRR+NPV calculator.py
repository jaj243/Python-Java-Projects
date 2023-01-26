import numpy as np
from scipy.optimize import root_scalar

def irr(cashflows):
    result = root_scalar(lambda r: np.npv(r, cashflows),  bracket=[0,1])
    irr = result.root
    npv = np.npv(irr, cashflows)
    return irr,npv

cashflows = [-100, 39, 59, 55, 20]
irr,npv = irr(cashflows)
print("Internal Rate of Return:", irr)
print("Net Present Value:", npv)
