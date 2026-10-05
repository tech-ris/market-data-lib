from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import date

@dataclass(frozen=True)
class Instrument(ABC):
    ticker: str
    currency: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "ticker", self.ticker.replace(" ", "").upper())
        if not self.ticker: raise ValueError("Missing ticker")

        object.__setattr__(self, "currency", self.currency.replace(" ", "").upper())
        if not self.currency: raise ValueError("Missing currency")
        if not self.currency.isalpha() or len(self.currency) != 3:
            raise ValueError("Currency must have three letters")

    @abstractmethod
    def price(self) -> float | NotImplementedError:
        """Price definition must be determined at sub-instrument level"""
        pass

@dataclass(frozen=True)
class Equity(Instrument):
    adj_price: float
    shares_outstanding: int

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.adj_price <= 0: raise ValueError("Stock price must be positive")
        if self.shares_outstanding <= 0: raise ValueError("Number of outstanding shares must be positive")

    def price(self) -> float:
        return self.adj_price

    @property
    def market_cap(self) -> float:
        return self.price() * self.shares_outstanding

@dataclass(frozen=True)
class Bond(Instrument):
    face_value: int
    coupon_rate: float
    years_to_maturity: int
    market_price: float

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.face_value <= 0: raise ValueError("Bond's face value must be positive")
        if self.coupon_rate <= 0: raise ValueError("Bond's coupon rate must be positive")
        if self.years_to_maturity <= 0: raise ValueError("Bond's years to maturity must be positive")
        if self.market_price <= 0: raise ValueError("Bond's market price must be positive")

    def price(self) -> float:
        """
        Market prices are commonly quoted in percentage of face value
        So to get the price of the bond, it must be multiplied by the face value 
        """
        return round(self.face_value * self.market_price/100, 2)

    @property
    def ytm(self) -> float:
        coupon = self.face_value * self.coupon_rate
        avg_annual_return = coupon + (self.face_value - self.price()) / self.years_to_maturity
        avg_capital_invested = (self.face_value + self.price()) / 2
        return round(avg_annual_return / avg_capital_invested, 4)

@dataclass(frozen=True)
class Option(Instrument):
    underlying: Equity
    option_type: str
    strike: float
    expiry: date

    def __post_init__(self) -> None:
        super().__post_init__()
        if not isinstance(self.underlying, Equity): raise TypeError("The underlying must be an Equity object")

        cleaned_option_type = self.option_type.replace(" ", "").lower() 
        if cleaned_option_type in {"call", "c"}:
            object.__setattr__(self, "option_type", "Call")
        elif cleaned_option_type in {"put", "p"}:
            object.__setattr__(self, "option_type", "Put")
        else:
            raise ValueError("Must be either call (c) or put (p)")

        if self.strike <= 0: raise ValueError("Strike price must be positive")

    def price(self) -> float | NotImplementedError:
        return NotImplementedError("Pricing not yet implemented")