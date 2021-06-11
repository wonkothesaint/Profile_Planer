from collections import namedtuple
Bracket = namedtuple("Bracket", "start pct")

tax_brackets = [Bracket(0, 10),
                Bracket(6290, 14),
                Bracket(9030, 20),
                Bracket(14490, 31),
                Bracket(20140, 35),
                Bracket(41910, 47),
                Bracket(53970, 50)]
surtax = Bracket(647640, 50)
ishtalmut_ceiling = 1571.2
pension_ceiling = 4326.0
credit_for_pension_insurance = 616 * 0.35
credit_point = 219
# 60% שכר ממוצע לפי סעיף 2
insurance_ceiling = 6331
health_insurance_brackets = [Bracket(0, 3.1), Bracket(insurance_ceiling, 5)]
national_insurance_brackets = [Bracket(0, 0.4), Bracket(insurance_ceiling, 7)]


def calc_brackets_sum(value, table):
    tax = 0
    i = 1
    while i < len(table) and table[i].start < value:
        tax += (table[i].start - table[i - 1].start) * table[i - 1].pct / 100
        i += 1
    return tax + (value - table[i - 1].start) * table[i - 1].pct / 100
