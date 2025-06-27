class UserProfile:
    def __init__(self, name, age, retirement_year, risk_tolerance):
        self.name = name
        self.age = age
        self.retirement_year = retirement_year
        self.risk_tolerance = risk_tolerance  # "Conservative", "Moderate", "Aggressive"

    def years_to_retire(self, current_year):
        return max(self.retirement_year - current_year, 0)

    def equity_target(self, current_year):
        yrs = self.years_to_retire(current_year)
        glide = min(1.0, max(0.3, yrs / 40))  # 30%–100% based on years to retirement
        multiplier = {
            "Aggressive": 1.0,
            "Moderate": 0.75,
            "Conservative": 0.5
        }[self.risk_tolerance]
        return round(glide * multiplier, 2)
