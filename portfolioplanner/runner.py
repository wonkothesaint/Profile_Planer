import Portfolio
import Salary
import json
from pathlib import Path


period = {
    "duration": 12,
    "pay_debts": [],
    "default_invest": "IBKR",
    "severance_plan": {
        "pension_rewards": "Pension S&P",
        "above_pension_rewards": "Gemel S&P",
        "above_pension_compensation": "Gemel 50plus",
        "ishtalmut": "Keren Ishtalmut",
    },
}
# Zainka
# period = {
#     "duration": 12,
#     "pay_debts": [],
#     "default_invest": "IBKR",
#     "severance_plan": {
#         "pension_rewards": "Pension",
#         "pension_compensation": "Pension",
#         "above_pension_rewards": "Pension Makifa",
#         "above_pension_compensation": "Pension Makifa",
#         "ishtalmut": "Keren Ishtalmut",
#     },
# }

user = "Wonko"
expenses = 6000

dirname = Path(__file__).parent
project_dir = dirname.parent
database_dir = project_dir / "database"
salary_path = database_dir / user / "salary.json"
assets_path = database_dir / user / "assets.json"
debts_path = database_dir / user / "debts.json"
salary_args = json.loads(salary_path.read_text())
assets_args = json.loads(assets_path.read_text())
debts_args = json.loads(debts_path.read_text())


salary = Salary.Salary(**salary_args)
print(salary.gross)
print(salary.net)
print(salary.severances)

portfolio = Portfolio.Portfolio()
for asset in assets_args:
    portfolio.add_asset(asset, assets_args[asset])
for debt in debts_args:
    portfolio.add_debt(debt, debts_args[debt])

# Portfolio.add_asset(asset)
plan = [period]

print(portfolio.short_report())
for period in plan:
    for month in range(period["duration"]):
        money_pool = 0
        money_pool += salary.net
        for severance in salary.severances:
            if severance in period["severance_plan"]:
                portfolio.invest_asset(
                    period["severance_plan"][severance], salary.severances[severance]
                )
            elif salary.severances[severance] > 0:
                raise Exception('Unplanned severance: ' + severance +
                                ' with monthly ' + str(salary.severances[severance]))
        money_pool += portfolio.progress_month()

        money_pool -= expenses

        portfolio.invest_asset(
            period["default_invest"], money_pool
        )

print(portfolio.short_report())