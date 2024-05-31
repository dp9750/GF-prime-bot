WEEKLY_GROSS_PERCENT = 0.0293  # 2,93 %
PROFIT_SHARES = {
    100: 0.50,
    500: 0.60,
    1500: 0.65,
    5000: 0.70,
    10000: 0.75,
    25000: 0.80,
    50000: 0.85,
}


class PrimeCalculator:

    def __init__(self) -> None:
        self.investment: float = 0
        self.weekly_gross_percent: float = WEEKLY_GROSS_PERCENT

    def get_profit_share(self, investment: float) -> float:
        keys = list(PROFIT_SHARES.keys())

        for i, minimum_investment in enumerate(keys[1:]):
            if investment < minimum_investment:
                return PROFIT_SHARES[keys[i]]

        return PROFIT_SHARES[keys[-1]]

    def weekly_net_profit(self) -> float:
        profit_share = self.get_profit_share(self.investment)
        net_weekly_profit = self.investment * self.weekly_gross_percent * profit_share
        return net_weekly_profit
