from portfolioplanner import Tax


class Salary:
    def __init__(
        self,
        gross,
        yearly_bonus,
        credit_points,
        rewards_pct=None,
        compensation_pct=None,
        ishtalmut_pct=None,
        pension_ceiling=Tax.pension_ceiling,
        ishtalmut_ceiling=Tax.ishtalmut_ceiling,
        is_rewards_compensation_seperated=True,
    ):
        self.gross = gross
        self.yearly_bonus = yearly_bonus
        self.credit_points = credit_points
        self.rewards_pct = rewards_pct
        self.compensation_pct = compensation_pct
        self.ishtalmut_pct = ishtalmut_pct

        self.pension_ceiling = pension_ceiling
        self.ishtalmut_ceiling = ishtalmut_ceiling
        self.is_rewards_compensation_seperated = is_rewards_compensation_seperated

        self.calculate_all_params()

    def update(
        self,
        gross=None,
        yearly_bonus=None,
        credit_points=None,
        rewards_pct=None,
        compensation_pct=None,
        ishtalmut_pct=None,
        pension_ceiling=None,
        ishtalmut_ceiling=None,
        is_rewards_compensation_seperated=None,
    ):
        if gross is not None:
            self.gross = gross
        if yearly_bonus is not None:
            self.yearly_bonus = yearly_bonus
        if credit_points is not None:
            self.credit_points = credit_points
        if rewards_pct is not None:
            self.rewards_pct = rewards_pct
        if compensation_pct is not None:
            self.compensation_pct = compensation_pct
        if ishtalmut_pct is not None:
            self.ishtalmut_pct = ishtalmut_pct
        if pension_ceiling is not None:
            self.pension_ceiling = pension_ceiling
        if ishtalmut_ceiling is not None:
            self.ishtalmut_ceiling = ishtalmut_ceiling
        if is_rewards_compensation_seperated is not None:
            self.is_rewards_compensation_seperated = is_rewards_compensation_seperated
        self.calculate_all_params()

    def calculate_all_params(self):
        self.rewards = self.calc_rewards()
        self.compensation = self.calc_compensation()
        self.ishtalmut = self.calc_ishtalmut()
        self.taxable_gross = self.calc_taxable_gross()
        self.net = self.calc_net()
        self.severances = self.calc_severances()

    def calc_taxable_gross(self):
        taxable_gross = self.gross
        taxable_gross += self.yearly_bonus / 12
        ishtalmut_taxable = self.gross * self.ishtalmut_pct["employer"] / 100
        ishtalmut_taxable -= Tax.ishtalmut_ceiling * self.ishtalmut_pct["employer"] / 10
        taxable_gross += max(ishtalmut_taxable, 0)

        return taxable_gross

    def calc_net(self):
        tax = 0
        tax += Tax.calc_brackets_sum(self.taxable_gross, Tax.tax_brackets)
        tax += Tax.calc_brackets_sum(
            self.taxable_gross, Tax.national_insurance_brackets
        )
        tax += Tax.calc_brackets_sum(self.taxable_gross, Tax.health_insurance_brackets)
        tax -= Tax.credit_point * self.credit_points
        tax -= Tax.credit_for_pension_insurance

        severance = 0
        severance += self.gross * self.ishtalmut_pct["employee"] / 100
        severance += self.gross * self.rewards_pct["employee"] / 100

        taxable_ishtalmut_not_int_net = (
            min(self.ishtalmut_ceiling, self.ishtalmut) - Tax.ishtalmut_ceiling
        )

        return self.taxable_gross - taxable_ishtalmut_not_int_net - tax - severance

    @staticmethod
    def get_severance_pct(severance_pct):
        pct = 0
        if "employer" in severance_pct:
            pct += severance_pct["employer"]
        if "employee" in severance_pct:
            pct += severance_pct["employee"]
        return pct

    def calc_rewards(self):
        return self.gross * self.get_severance_pct(self.rewards_pct) / 100

    def calc_compensation(self):
        return self.gross * self.get_severance_pct(self.compensation_pct) / 100

    def calc_ishtalmut(self):
        return self.gross * self.get_severance_pct(self.ishtalmut_pct) / 100

    def calc_severances(self):
        severances = {}
        if not self.is_rewards_compensation_seperated:
            severances["pension"] = min(
                self.rewards + self.compensation, self.pension_ceiling
            )
            severances["above_pension"] = (
                self.rewards + self.compensation - severances["pension"]
            )
        else:
            severances["pension_rewards"] = min(self.rewards, self.pension_ceiling)
            severances["pension_compensation"] = min(
                self.compensation, self.pension_ceiling - severances["pension_rewards"]
            )
            severances["above_pension_rewards"] = (
                self.rewards - severances["pension_rewards"]
            )
            severances["above_pension_compensation"] = (
                self.compensation - severances["pension_compensation"]
            )
        severances["ishtalmut"] = min(self.ishtalmut, self.ishtalmut_ceiling)
        return severances
