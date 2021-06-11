# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 09:07:21 2021

@author: wonko
"""

import Profile
import Salary
import Utils

ibkr_args = {'value': 797625,
             'deposit_fee': 0,
             'management_fees_yearly': 0.06,
             'yield_yearly': 7.17,
             'dividends_yield_yearly': 1.6,
             'tax': 25,
             'tax_dividends': 25,
             'taxable': 200000}

salary_args = {'gross': 38800,
               'yearly_bonus': 55500,
               'credit_points': 2.25,
               'rewards_percents': {'name': 'Gemel',
                                    'employer': 6.5,
                                    'employee': 6},
               'compensation_percents': {'name': 'Gemel_compensation',
                                         'employer': 8.33},
               'ishtalmut_percents': {'name': 'Keren_ishtalmut',
                                      'employer': 7.5,
                                      'employee': 2.5}
               }

period = {'duration': 10,
          'pay_debts': [],
          'default_invest': 'IBKR',
          'severance_plan': {'pension_rewards': 'pension',
                             'gemel_rewards': 'gemel_rewards',
                             'gemel_compensation': 'gemel_compensation'}
          }

expenses = 6000

salary = Salary.Salary(**salary_args)
print(salary.net)
print(salary.taxable_gross)
print(salary.severances)


profile = Profile.Profile()
profile.add_asset('pension', ibkr_args)
profile.add_asset('gemel_rewards', ibkr_args)
profile.add_asset('gemel_compensation', ibkr_args)
profile.add_asset('IBKR', ibkr_args)
# Profile.add_asset(asset)
plan = [period]

money_pool = 0
for period in plan:
    for month in range(period['duration']):
        money_pool += salary.net
        for severance in period['severance_plan'].keys():
            profile.invest_asset(period['severance_plan'][severance], salary.severances[severance])
        money_pool += profile.progress_month()
        # print(money_pool)
        # print(profile.assets['IBKR'].value)

        # pay_debts = period['pay_debts']
        # for debt in pay_debts.keys():
        #     Profile.pay_debt(debt,pay_debts[debt])
        #
        # Profile.invest_asset(period['default_invest'], money_pool)
