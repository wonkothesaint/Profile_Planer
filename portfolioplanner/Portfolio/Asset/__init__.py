from portfolioplanner.Utils import *


class Asset:
    def __init__(
            self,
            value,
            yield_yearly_pct=0,
            dividends_yield_yearly_pct=0,
            deposit_fee_pct=0,
            management_fees_yearly_pct=0,
            tax_dividends_pct=0,
            tax_pct=0,
            gains=0,
    ):
        self.value = value
        self.yield_yearly_pct = yield_yearly_pct
        self.dividends_yield_yearly_pct = dividends_yield_yearly_pct
        self.deposit_fee_pct = deposit_fee_pct
        self.management_fees_yearly_pct = management_fees_yearly_pct
        self.tax_dividends_pct = tax_dividends_pct
        self.tax_pct = tax_pct
        self.gains = gains

    # progress value and returns earned money
    def progress_month(self):
        value = self.value
        yield_monthly = (value * self.yield_yearly_pct - value * self.management_fees_yearly_pct) / 1200
        self.value += yield_monthly
        self.gains += yield_monthly
        dividends_monthly = value * self.dividends_yield_yearly_pct * self.tax_dividends_pct / 120000
        return dividends_monthly

    def deposit(self, amount):
        self.value += amount

    def calc_value_after_tax(self):
        return self.value - (self.gains * self.tax_pct / 100)

    def __str__(self):
        return currency_str(self.value) + ' before tax. ' + \
               currency_str(self.calc_value_after_tax(self)) + \
               ' after tax.'
