from profileplanner.Profile import Asset


class Profile:
    def __init__(self):
        self.assets = {}
        self.debts = {}

    def add_asset(self, name, asset_args):
        self.assets[name] = Asset.Asset(**asset_args)

    def invest_asset(self, name, amount):
        self.assets[name].value += amount

    def progress_month(self):
        money_pool = 0
        for asset in self.assets:
            money_pool += self.assets[asset].progress_month()
        for debt in self.debts:
            money_pool -= self.debts[debt].progress_month()
        return money_pool
