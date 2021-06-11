tax_table = [(0, 10), (6290, 14), (9030, 20), (14490, 31), (20140, 35), (41910, 47), (53970, 50)]
surtax = (647640, 50)
ishtalmut_ceiling = 1571.2
pension_ceiling = 4326.0
credit_for_pension_insurance = 616 * 0.35
credit_point = 219
# 60% שכר ממוצע לפי סעיף 2
insurance_ceiling = 6331
health_insurance = [(0, 3.1), (insurance_ceiling, 5)]
national_insurance = [(0, 0.4), (insurance_ceiling, 7)]


def calc_tax(taxable, table):
    tax = 0
    i = 1
    while i < len(table) and table[i][0] < taxable:
        tax += (table[i][0] - table[i - 1][0]) * table[i - 1][1] / 100
        i += 1
    return tax + (taxable - table[i - 1][0]) * table[i - 1][1] / 100
