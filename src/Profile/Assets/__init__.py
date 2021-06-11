# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 09:07:21 2021

@author: wonko
"""

def percents_yearly_to_monthly(yearly_percent):
    return ((1+yearly_percent)**(1/12))-1

class Asset:
    def __init__(self, name: str, value: int, 
                 default_deposit_monthly: int, deposit_fee: int,
                 management_fees: int, 
                 yield_yearly: int, dividends_yearly: int,
                 value_for_tax: int, tax: int):
        self._value = value
        self._deposit = default_deposit_monthly
        self._deposit_fee = deposit_fee
        self._management_fees = yearly_to_monthly(management_fees/100)
        self._yield = yearly_to_monthly(yield_yearly/100)
        self._dividends = yearly_to_monthly(dividends_yearly/100)
        self._value_for_tax = value_for_tax
        self._tax = tax
    
    # Return the number of years of using 'withdraw' before asset is depleted.
    # Dividends are not taken into account.
    def calc_depletion(self, withdraw: int, deposit = 0):
        pass
    
    def get_dividends(self):
        return self._value*self._dividends
    
    def grow_month(self, deposit = None):
        if deposit == None:
            deposit = self._deposit
        self._value += deposit*(1-self._deposit_fee)
        self._value *= (1+(self._yield - self._management_fees))
    
class debt:
    def __init__(self, name: str, value: int, interest_yearly: int, months: int, loan_type=0):
        self._value = value
        self._interest_yearly = interest_yearly
        self._months = months
        self._loan_type = loan_type
        
        self._interest_value = value*(1 + interest_yearly)**(months/12)
        self._payment_loan = value / months
        self._payment_interest = interest_value / months
        
    def get_payment(self):
        return self._payment_loan + self._payment_interest
    
    def pay_month(self):
        self._value -= self._payment_loan
        self._interest_value -= self._interest_value
        self._months -= 1
        
        
class retirement_planner:
    
    def __init__(self, assets: list, debts: list, money_pool = 0):
        self._assets = assets
        self._debts = debts
        self._salary = []
        self._living_cost = []
        self._money_pool = money_pool
      
    def get_cashflow(self):
        cashflow = 0
        for asset in self._assets:
            cashflow += asset.get_dividends()
        for debt in self._debts:
            cashflow -= debt.get_payment()
    
    # 'living_cost' should indicate jumps in costs through life.
    # For example [(10: 10000), (5:15000)] means 10 years of 10k cost 
    # and 5 years of 15k cost.
    # Similarly, salary.
    def plan_retirement(self, salary: list, living_cost: list):
        pass
    
    
IBKR = Asset('IBKR', 797625, 17000, 0, 0.06, 7.17, 1.6, 0, 0)

for i in range(360):
    print(IBKR._value)
    IBKR.grow_month()
    
    
    
    
    
    
    
    
    
    
    
    
    
    