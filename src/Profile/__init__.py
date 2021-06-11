class Asset:
    def __init__(self, value,
                 yield_yearly, dividends_yield_yearly,
                 deposit_fee, management_fees_yearly,
                 tax_dividends, tax, taxable):
        self.value = value
        self.yield_yearly = yield_yearly
        self.dividends_yield_yearly = dividends_yield_yearly
        self.deposit_fee = deposit_fee
        self.management_fees_yearly = management_fees_yearly
        self.tax_dividends = tax_dividends
        self.tax = tax
        self.taxable = taxable

    # progress value and returns earned money
    def progress_month(self):
        value = self.value
        self.value += value * self.yield_yearly/1200
        self.value -= value * self.management_fees_yearly / 1200
        return value * self.dividends_yield_yearly * self.tax_dividends / 120000


class Profile:
    def __init__(self):
        self.assets = {}
        self.debts = {}

    def add_asset(self, name, asset_args):
        self.assets[name] = Asset(**asset_args)

    def invest_asset(self, name, amount):
        self.assets[name].value += amount

    def progress_month(self):
        money_pool = 0
        for asset in self.assets:
            money_pool += self.assets[asset].progress_month()
        for debt in self.debts:
            money_pool -= self.debts[debt].progress_month()
        return money_pool

