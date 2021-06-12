from profileplanner.Profile import Asset


class Profile:
    def __init__(self):
        self.assets = {}
        self.debts = {}

    def add_asset(self, name, asset_args):
        self.assets[name] = Asset.Asset(**asset_args)

    def invest_asset(self, name, amount):
        self.assets[name].deposit(amount)

    def progress_month(self):
        money_pool = 0
        for asset in self.assets:
            money_pool += self.assets[asset].progress_month()
        for debt in self.debts:
            money_pool -= self.debts[debt].progress_month()
        return money_pool

    def short_report(self):
        total_before_tax = 0
        total_after_tax = 0
        for asset in self.assets:
            total_before_tax += self.assets[asset].value
            total_after_tax += self.assets[asset].calc_value_after_tax()
        asset_string = 'Asset total: \n\tBefore tax: ' + str(total_before_tax) + '\n\tAfter tax: ' + str(total_after_tax) + '\n'
        debts_string = ''
        for debt in self.debts:
            pass
            # debts_string += debt + ': ' + str(self.debts[debt]) + '\n'
        return asset_string + debts_string + \
               'Total: \n\tBefore tax: ' + str(total_before_tax) + '\n\tAfter tax: ' + str(total_after_tax) + '\n'

    def full_report(self):
        total_before_tax = 0
        total_after_tax = 0
        asset_string = 'Assets:\n'
        for asset in self.assets:
            total_before_tax += self.assets[asset].value
            total_after_tax += self.assets[asset].calc_value_after_tax()
            asset_string += asset + ': ' + str(self.assets[asset]) + '\n'
        debts_string = 'Debts:\n'
        for debt in self.debts:
            pass
            # debts_string += debt + ': ' + str(self.debts[debt]) + '\n'
        return asset_string + debts_string + str(self)
