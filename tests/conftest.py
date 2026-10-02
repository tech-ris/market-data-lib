from market_data_lib.instruments import Instrument, Equity, Bond, Option
from market_data_lib.portfolio import Portfolio
from collections.abc import Callable
from datetime import date
import pytest


# Default values for default instance. 
# Will be used along with overrides throughout the test series

DEFAULT_VALUES_INSTRUMENT = {"ticker": "INSTR", "currency": "CUR"}
DEFAULT_VALUES_EQUITY = DEFAULT_VALUES_INSTRUMENT | {"ticker":"STCK", "adj_price": 150, "shares_outstanding": 400_000}
DEFAULT_VALUES_BOND = DEFAULT_VALUES_INSTRUMENT | {"ticker":"BND", "face_value": 1000, "coupon_rate": 0.05, "years_to_maturity": 10, "market_price": 98.72}

@pytest.fixture
def default_equity() -> Callable:
    def _called_func(**overrides) -> Equity:
        args_tested = DEFAULT_VALUES_EQUITY | overrides
        return Equity(**args_tested) # type: ignore
    return _called_func

@pytest.fixture
def default_bond() -> Callable:
    def _called_func(**overrides) -> Bond:
        args_tested = DEFAULT_VALUES_BOND | overrides
        return Bond(**args_tested) # type: ignore
    return _called_func


DEFAULT_VALUES_OPTION = DEFAULT_VALUES_INSTRUMENT | {"ticker":"OPT", "option_type": "C", "strike": 175, "expiry": date(2027,12,31)}
@pytest.fixture
def default_option(default_equity) -> Callable:
    DEFAULT_VALUES_OPTION_LOCAL = DEFAULT_VALUES_OPTION | {"underlying": default_equity()}
    def _called_func(**overrides) -> Option:
        args_tested = DEFAULT_VALUES_OPTION_LOCAL | overrides
        return Option(**args_tested) # type: ignore
    return _called_func


@pytest.fixture
def default_pf(default_equity, default_bond) -> Callable:
    DEFAULT_VALUES_PF = {default_equity(): 10, default_bond(): 2}
    def _called_func(overrides: dict[Instrument, float] = {}) -> Portfolio:
        args_tested = DEFAULT_VALUES_PF | overrides
        return Portfolio(args_tested)
    return _called_func