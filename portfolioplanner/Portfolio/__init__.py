from portfolioplanner.Portfolio import Asset
from portfolioplanner.Portfolio import Debt


class Portfolio:
    def __init__(self):
        self.assets = {}
        self.debts = {}
        self.cashflow_in = 0
        self.cashflow_out = 0

    def add_debt(self, name, debt_args):
        self.debts[name] = Debt.Debt(**debt_args)

    def add_asset(self, name, asset_args):
        self.assets[name] = Asset.Asset(**asset_args)

    def buy_asset(self, name, amount):
        self.assets[name].buy(amount)

    def sell_asset(self, name, amount):
        self.assets[name].sell(amount)

    def progress_month(self):
        self.cashflow_in = 0
        self.cashflow_out = 0
        for asset in self.assets:
            self.cashflow_in += self.assets[asset].progress_month()
        closed_debts = []
        for debt in self.debts:
            self.cashflow_out -= self.debts[debt].progress_month()
            if self.debts[debt].is_closed():
                closed_debts.append(debt)
        for debt in closed_debts:
            self.debts.pop(debt)
        return self.cashflow_in + self.cashflow_out

    def short_report(self):
        total_before_tax = 0
        total_after_tax = 0
        for asset in self.assets:
            total_before_tax += self.assets[asset].value
            total_after_tax += self.assets[asset].calc_value_after_tax()
        asset_string = (
            "Asset total: \n\tBefore tax: "
            + str(int(total_before_tax))
            + "\n\tAfter tax: "
            + str(int(total_after_tax))
            + "\n"
        )
        debt_to_pay = 0
        for debt in self.debts:
            debt_to_pay += self.debts[debt].ammount
        debts_string = "Debt total: " + str(int(debt_to_pay)) + "\n"
        return (
            asset_string
            + debts_string
            + "Total: \n\tBefore tax: "
            + str(int(total_before_tax - debt_to_pay))
            + "\n\tAfter tax: "
            + str(int(total_after_tax - debt_to_pay))
            + "\n"
        )

    def full_report(self):
        total_before_tax = 0
        total_after_tax = 0
        asset_string = "Assets:\n"
        for asset in self.assets:
            total_before_tax += self.assets[asset].value
            total_after_tax += self.assets[asset].calc_value_after_tax()
            asset_string += asset + ": " + str(self.assets[asset]) + "\n"
        debts_string = "Debts:\n"
        for debt in self.debts:
            pass
            # debts_string += debt + ': ' + str(self.debts[debt]) + '\n'
        return asset_string + debts_string + str(self)
