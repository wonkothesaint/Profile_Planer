class Debt():
    def __init__(self,
                 loan_type,
                 ammount,
                 interest,
                 duration=0,
                 date_start=None,
                 currency="ILS"):
        self.loan_type = loan_type
        self.ammount = ammount
        self.interest = interest / 1200  # yearly to monthly pct
        self.duration = duration
        self.date_start = date_start
        self.currency = currency

        self.months_left = duration
        if self.loan_type == 'Spicher':
            self.monthly_payment = self.ammount * Debt.calc_spicher_monthly_pct(self.interest, self.duration)
        self.interest_ammount = self.calc_initial_interest_ammount()
        self.closed = False

    @staticmethod
    def calc_spicher_monthly_pct(interest, duration):
        # print(interest, duration)
        if interest > 0:
            # print(interest / (1 - ((1 + interest) ** - duration)))
            return interest / (1 - ((1 + interest) ** - duration))
        # print(1 / duration)
        return 1 / duration

    def calc_initial_interest_ammount(self):
        if self.loan_type == 'Spicher':
            return self.duration * self.monthly_payment - self.ammount
        return 0

    def calc_next_payment(self):
        if self.loan_type == 'Spicher':
            return self.monthly_payment
        return 0

    def close_debt(self):
        self.closed = True
        return self.ammount + self.interest_ammount

    def is_closed(self):
        return self.closed

    def progress_month(self):
        if self.months_left > self.duration:
            return 0

        if self.loan_type == 'Margin':
            self.ammount += self.ammount * self.interest
            return 0

        pay_debt = 0
        pay_interest = 0
        if self.loan_type == 'Spicher':
            pay_debt = self.monthly_payment * (1 / (Debt.calc_spicher_monthly_pct(self.interest, self.months_left)) -
                                            (1 / Debt.calc_spicher_monthly_pct(self.interest, self.months_left - 1)))
            # print(self.monthly_payment, pay_debt)
            pay_interest = self.monthly_payment - pay_debt
        self.ammount -= pay_debt
        self.interest_ammount -= pay_interest
        self.months_left -= 1
        if self.months_left <= 0:
            self.closed = True
        return pay_debt + pay_interest
