from abc import ABC, abstractmethod

# Instrument
class Instrument(ABC):
    def __init__(self, ticker: str, currency: str):
        ticker = ticker.replace(" ","").upper()
        if ticker == "": raise ValueError("Missing ticker")
        self.ticker = ticker

        currency = currency.replace(" ","").upper()
        if currency == "": raise ValueError("Missing currency")
        if not currency.isalpha() or len(currency) != 3: 
            raise ValueError("Currency must have three letters")
        self.currency = currency

    @property
    @abstractmethod
    def price(self):
        """Price definition must be determined at sub-instrument level"""
        pass

# Equity
class Equity(Instrument):
    def __init__(self, ticker: str, currency: str, adj_price: float, shares_outstanding: int) -> None:
        super().__init__(ticker, currency)

        if adj_price <= 0: 
            raise ValueError("Stock price must be strictly positive")
        self.adj_price = adj_price

        if shares_outstanding <= 0: 
            raise ValueError("Number of outstanding shares must be strictly positive")
        self.shares_outstanding = shares_outstanding

    def __repr__(self):
        return f"Equity({self.ticker},{self.currency},{self.adj_price},{self.shares_outstanding})"

    def price(self):
        return self.adj_price

    @property
    def market_cap(self):
        return self.shares_outstanding * self.adj_price