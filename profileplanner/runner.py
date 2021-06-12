import Profile
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

user = "wonko"
expenses = 6000

dirname = Path(__file__).parent
project_dir = dirname.parent
database_dir = project_dir / "database"
salary_path = database_dir / user / "salary.json"
assets_path = database_dir / user / "assets.json"
salary_args = json.loads(salary_path.read_text())
assets_args = json.loads(assets_path.read_text())


salary = Salary.Salary(**salary_args)

profile = Profile.Profile()
for asset in assets_args:
    profile.add_asset(asset, assets_args[asset])

# Profile.add_asset(asset)
plan = [period]

print(profile.short_report())
for period in plan:
    for month in range(period["duration"]):
        money_pool = 0
        money_pool += salary.net
        for severance in salary.severances:
            if severance in period["severance_plan"]:
                profile.invest_asset(
                    period["severance_plan"][severance], salary.severances[severance]
                )
            elif salary.severances[severance] > 0:
                raise Exception('Unplanned severance: ' + severance +
                                ' with monthly ' + str(salary.severances[severance]))
        money_pool += profile.progress_month()
        profile.invest_asset(
            period["default_invest"], money_pool
        )

print(profile.short_report())
        # pay_debts = period['pay_debts']
        # for debt in pay_debts:
        #     Profile.pay_debt(debt,pay_debts[debt])
        #
        # Profile.invest_asset(period['default_invest'], money_pool)
