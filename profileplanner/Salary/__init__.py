import profile_planner.Tax as Tax


class Salary:
    def __init__(self, gross, yearly_bonus, credit_points,
                 rewards_percents=None, compensation_percents=None, ishtalmut_percents=None,
                 pension_ceiling=Tax.pension_ceiling, ishtalmut_ceiling=Tax.ishtalmut_ceiling,
                 is_rewards_compensation_seperated=True):
        self.gross = gross
        self.yearly_bonus = yearly_bonus
        self.credit_points = credit_points
        self.rewards_percents = rewards_percents
        self.compensation_percents = compensation_percents
        self.ishtalmut_percents = ishtalmut_percents

        self.pension_ceiling = pension_ceiling
        self.ishtalmut_ceiling = ishtalmut_ceiling
        self.is_rewards_compensation_seperated = is_rewards_compensation_seperated

        self.rewards = self.calc_rewards()
        self.compensation = self.calc_compensation()
        self.ishtalmut = self.calc_ishtalmut()
        self.taxable_gross = self.calc_taxable_gross()
        self.net = self.calc_net()
        self.severances = self.calc_severances()

    def calc_taxable_gross(self):
        taxable_gross = self.gross
        taxable_gross += self.yearly_bonus / 12
        ishtalmut_taxable = self.gross * self.ishtalmut_percents['employer'] / 100
        ishtalmut_taxable -= Tax.ishtalmut_ceiling * self.ishtalmut_percents['employer'] / 10
        taxable_gross += max(ishtalmut_taxable, 0)

        return taxable_gross

    def calc_net(self):
        tax = 0
        tax += Tax.calc_tax(self.taxable_gross, Tax.tax_table)
        tax += Tax.calc_tax(self.taxable_gross, Tax.national_insurance)
        tax += Tax.calc_tax(self.taxable_gross, Tax.health_insurance)
        tax -= Tax.credit_point * self.credit_points
        tax -= Tax.credit_for_pension_insurance

        severance = 0
        severance += self.gross * self.ishtalmut_percents['employee'] / 100
        severance += self.gross * self.rewards_percents['employee'] / 100

        taxable_ishtalmut_not_int_net = (min(self.ishtalmut_ceiling, self.ishtalmut) - Tax.ishtalmut_ceiling)

        return self.taxable_gross - taxable_ishtalmut_not_int_net - tax - severance

    @staticmethod
    def get_severance_percent(severance_percent):
        percent = 0
        if 'employer' in severance_percent:
            percent += severance_percent['employer']
        if 'employee' in severance_percent:
            percent += severance_percent['employee']
        return percent

    def calc_rewards(self):
        return self.gross * self.get_severance_percent(self.rewards_percents) / 100

    def calc_compensation(self):
        return self.gross * self.get_severance_percent(self.compensation_percents) / 100

    def calc_ishtalmut(self):
        return self.gross * self.get_severance_percent(self.ishtalmut_percents) / 100

    def calc_severances(self):
        severances = {}
        if not self.is_rewards_compensation_seperated:
            severances['pension'] = min(self.rewards + self.compensation, self.pension_ceiling)
            severances['above_pension'] = self.rewards + self.compensation - severances['pension']
        else:
            severances['pension_rewards'] = min(self.rewards, self.pension_ceiling)
            severances['pension_compensation'] = min(self.compensation,
                                                     self.pension_ceiling - severances['pension_rewards'])
            severances['above_pension_rewards'] = self.rewards - severances['pension_rewards']
            severances['above_pension_compensation'] = self.compensation - severances['pension_compensation']
        severances['ishtalmut'] = min(self.ishtalmut, self.ishtalmut_ceiling)
        return severances

