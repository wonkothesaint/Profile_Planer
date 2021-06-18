import Portfolio
import Salary
import json
from pathlib import Path
user = "Wonko"

dirname = Path(__file__).parent
project_dir = dirname.parent
user_database_dir = project_dir / "database" / user
salary_path = user_database_dir / "salary.json"
assets_path = user_database_dir / "assets.json"
debts_path = user_database_dir / "debts.json"
plan_path = user_database_dir / "plan.json"
salary_args = json.loads(salary_path.read_text())
assets_args = json.loads(assets_path.read_text())
debts_args = json.loads(debts_path.read_text())
plan = json.loads(plan_path.read_text())

salary = Salary.Salary(**salary_args)
expenses = 6000
portfolio = Portfolio.Portfolio()
for asset in assets_args:
    portfolio.add_asset(asset, assets_args[asset])
for debt in debts_args:
    portfolio.add_debt(debt, debts_args[debt])

for i in range(len(plan)):
    period = plan['period' + str(i)]
    if 'salary' in period:
        salary.update(**period['salary'])

    print('Period ' + str(i))
    print('Gross salary: ' + str(salary.gross))
    print('Net salary: ' + str(int(salary.net)))
    print('Total severances: ' + str(int(sum(salary.severances.values()))))

    for month in range(period["duration"]):
        cashflow_in = 0
        cashflow_out = 0
        cashflow_in += salary.net
        for severance in salary.severances:
            if severance in period["severance_plan"]:
                portfolio.buy_asset(
                    period["severance_plan"][severance], salary.severances[severance]
                )
            elif salary.severances[severance] > 0:
                raise Exception('Unplanned severance: ' + severance +
                                ' with monthly ' + str(salary.severances[severance]))
        portfolio.progress_month()
        cashflow_in += portfolio.cashflow_in
        cashflow_out += portfolio.cashflow_out
        cashflow_out -= expenses

        cashflow = cashflow_in + cashflow_out
        if cashflow > 0:
            portfolio.buy_asset(
                period["default_buy"], cashflow
            )
        else:
            portfolio.sell_asset(
                period["default_sell"], cashflow
            )

    print('Cashflow: ' + str(int(cashflow_in)) + str(int(cashflow_out)) + '=' + str(int(cashflow)))
    print('After period ' + str(i))
    print(portfolio.short_report())
