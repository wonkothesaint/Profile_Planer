from collections import namedtuple

Bracket = namedtuple("Bracket", "start pct")
tax_brackets = [
    Bracket(0, 10),
    Bracket(6290, 14),
    Bracket(9030, 20),
    Bracket(14490, 31),
    Bracket(20140, 35),
    Bracket(41910, 47),
    Bracket(53970, 50),
]

surtax = Bracket(647640, 50)
ishtalmut_ceiling = 1571.2
pension_ceiling = 4326.0
credit_for_pension_insurance = 616 * 0.35
credit_point = 219
# 60% שכר ממוצע לפי סעיף 2
insurance_ceiling = 6331
health_insurance_brackets = [Bracket(0, 3.1), Bracket(insurance_ceiling, 5)]
national_insurance_brackets = [Bracket(0, 0.4), Bracket(insurance_ceiling, 7)]


def calc_brackets_sum(value, brackets):
    result = 0
    i = 1
    while i < len(brackets) and brackets[i].start < value:
        result += (brackets[i].start - brackets[i - 1].start) * brackets[i - 1].pct
        i += 1
    result += (value - brackets[i - 1].start) * brackets[i - 1].pct
    return result / 100

    # trying to write with bisec. not very beutiful.
    # brackets_start = [bracket.start for bracket in brackets]
    # brackets_diff = [brackets[i+1].start - brackets[i].start for i in range(len(brackets)-1)]
    # brackets_pct = [bracket.pct for bracket in brackets]
    # bracket = bisect.bisect_right(brackets_start, value)
    #
    # result = sum(diff * pct / 100 for diff, pct in zip(brackets_diff[bracket], brackets_pct))
    # result += value - brackets_start[bracket]
    # print(result)
    # return result
