from abc import ABC, abstractmethod
from datetime import date

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

    def __eq__(self, other):
        """Two are instruments are the same if they have the same ticker and currency"""
        if not isinstance(other, Instrument):
            return NotImplemented
        return self.ticker == other.ticker and self.currency == other.currency

    def __hash__(self):
        return hash((self.ticker, self.currency))

    @abstractmethod
    def price(self):
        """Price definition must be determined at sub-instrument level"""
        pass

# Equity
class Equity(Instrument):
    def __init__(self, ticker: str, currency: str, adj_price: float, shares_outstanding: int) -> None:
        super().__init__(ticker, currency)

        if adj_price <= 0: raise ValueError("Stock price must be strictly positive")
        self.adj_price = adj_price

        if shares_outstanding <= 0: raise ValueError("Number of outstanding shares must be strictly positive")
        self.shares_outstanding = shares_outstanding

    def __repr__(self) -> str:
        return f"Equity({self.ticker},{self.currency},{self.adj_price},{self.shares_outstanding})"

    def price(self) -> float:
        return self.adj_price

    @property
    def market_cap(self) -> float:
        return self.shares_outstanding * self.adj_price

# Bond
class Bond(Instrument):
    def __init__(self, ticker: str, currency: str, face_value: int, coupon_rate: float, years_to_maturity: int, market_price: float) -> None:
        super().__init__(ticker, currency)

        if face_value <= 0: raise ValueError("Bond's face value must be strictly positive")
        self.face_value = face_value
        if coupon_rate <= 0: raise ValueError("Bond's coupon rate must be strictly positive")
        self.coupon_rate = coupon_rate
        if years_to_maturity <= 0: raise ValueError("Bond's years to maturity must be strictly positive")
        self.years_to_maturity = years_to_maturity
        if market_price <= 0: raise ValueError("Bond's market price must be strictly positive")
        self.market_price = market_price

    def __repr__(self) -> str:
        return f"Bond({self.ticker}, {self.currency}, {self.face_value}, {self.coupon_rate}, {self.years_to_maturity}, {self.market_price})"

    def price(self) -> float:
        """
        Market prices are commonly quoted in percentage of Face Value
        So to get the price of the obligation, it must be multiplied by the face value
        """
        return round(self.face_value * self.market_price/100, 2)

    @property
    def ytm(self) -> float:
        coupon = self.face_value * self.coupon_rate
        avg_annual_return = coupon + (self.face_value - self.price()) / self.years_to_maturity
        avg_capital_invested = (self.face_value + self.price()) / 2
        return round(avg_annual_return / avg_capital_invested, 4)

class Option(Instrument):
    def __init__(self, ticker: str, currency: str, underlying: Equity, option_type: str, strike: float, expiry: date) -> None:
        super().__init__(ticker, currency)

        if not isinstance(underlying, Equity): raise TypeError("The underlying must be an Equity object")
        self.underlying = underlying

        if option_type.replace(" ","").lower() in {"call", "c"}:
            self.option_type = "Call"
        elif option_type.replace(" ","").lower() in {"put", "p"}:
            self.option_type = "Put"
        else:
            raise ValueError("Must be either call (c) or put (p)")

        if strike <= 0: raise ValueError("Strike price must be strictly positive")
        self.strike = strike
        self.expiry = expiry

    def __repr__(self) -> str:
        return f"Option({self.ticker}, {self.currency}, {self.underlying}, {self.option_type}, {self.strike}, {self.expiry})"

    def price(self):
        return NotImplementedError("Pricing not yet implemented")