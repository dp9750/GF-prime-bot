class PrimeBot:

    def __init__(self) -> None:
        self.investment: float = 0
        self.input_investment: bool = False

    def validate_investment(self, investment: str) -> bool:
        processed: float = 0

        try:
            processed = float(investment)
        except ValueError:
            return False

        return processed > 0
