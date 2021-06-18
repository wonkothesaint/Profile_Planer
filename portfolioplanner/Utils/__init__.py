def percents_yearly_to_monthly(yearly_percent):
    return ((1 + yearly_percent) ** (1 / 12)) - 1


def currency_str(number, currency="ILS"):
    if currency == "ILS":
        return "₪{:,.2f}".format(number)
    if currency == "USD":
        return "${:,.2f}".format(number)
    return "{:,.2f} ".format(number) + currency
