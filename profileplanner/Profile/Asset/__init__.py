class Asset:
    def __init__(
        self,
        value,
        yield_yearly,
        dividends_yield_yearly,
        deposit_fee,
        management_fees_yearly,
        tax_dividends,
        tax,
        taxable,
    ):
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
        self.value += value * self.yield_yearly / 1200
        self.value -= value * self.management_fees_yearly / 1200
        return value * self.dividends_yield_yearly * self.tax_dividends / 120000
