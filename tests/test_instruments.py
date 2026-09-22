from market_data_lib.instruments import Equity
from contextlib import nullcontext
import pytest

# Default values for default instance. 
# Will be used along with overrides throughout this test series

DEFAULT_VALUES: dict = {"ticker": "STCK",
                        "currency": "USD",
                        "adj_price": 150,
                        "shares_outstanding": 400_000
                        }

# Initial test: test of default behavior
def test_default_values():
    stock = Equity(**DEFAULT_VALUES)
    assert stock.ticker == DEFAULT_VALUES["ticker"]
    assert stock.currency == DEFAULT_VALUES["currency"]
    assert stock.adj_price == DEFAULT_VALUES["adj_price"]
    assert stock.shares_outstanding == DEFAULT_VALUES["shares_outstanding"]
    assert stock.price() == DEFAULT_VALUES["adj_price"]
    assert stock.market_cap == DEFAULT_VALUES["adj_price"] * DEFAULT_VALUES["shares_outstanding"]


# Use of fixture to create and use the default class object throughout testing
@pytest.fixture
def default_equity():
    def _called_func(**overrides):
        args_tested: dict = DEFAULT_VALUES | overrides
        return Equity(**args_tested)
    return _called_func


# TESTS
# Use of parametrize decorator to design several combinations for each class argument tested

# Ticker
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context", 
    [
        pytest.param(" S T    C K  ", "STCK", nullcontext(), id="No Whitespace"),
        pytest.param("  ", None, pytest.raises(ValueError, match="^Missing ticker$"), id="Empty ticker")
    ]
)
def test_ticker(default_equity, value_test, expected_value, expected_context) -> None:
    with expected_context:
        stock_test = default_equity(ticker=value_test)
        assert stock_test.ticker == expected_value

# Currency
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context", 
    [
        pytest.param(" U S    D  ", "USD", nullcontext(), id="No Whitespace"),    # No whitespace
        pytest.param("  ", None, pytest.raises(ValueError, match="^Missing currency$"), id="Empty currency"),
        pytest.param("U5D", None, pytest.raises(ValueError, match="^Currency must have three letters$"), id="Only letters"),
        pytest.param("US", None, pytest.raises(ValueError, match="^Currency must have three letters$"), id="Less than 3 letters"),
        pytest.param("USDD", None, pytest.raises(ValueError, match="^Currency must have three letters$"), id="More than 3 letters")
    ]
)
def test_currency(default_equity, value_test, expected_value, expected_context) -> None:
    with expected_context:
        stock_test = default_equity(currency=value_test)
        assert stock_test.currency == expected_value

# Adjusted Close Price
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context", 
    [
        pytest.param(0, None, pytest.raises(ValueError, match="^Stock price must be strictly positive$"), id="No null value"),
        pytest.param(-100, None, pytest.raises(ValueError, match="^Stock price must be strictly positive$"), id="No negative price")
    ]
)
def test_adj_price(default_equity, value_test, expected_value, expected_context) -> None:
    with expected_context:
        stock_test = default_equity(adj_price=value_test)
        assert stock_test.adj_price == expected_value

# Number of outstanding shares
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context", 
    [
        pytest.param(0, None, pytest.raises(ValueError, match="^Number of outstanding shares must be strictly positive$"), id="No null value"),
        pytest.param(-100, None, pytest.raises(ValueError, match="^Number of outstanding shares must be strictly positive$"), id="No negative number of outstanding shares")
    ]
)
def test_shares_outstanding(default_equity, value_test, expected_value, expected_context) -> None:
    with expected_context:
        stock_test = default_equity(shares_outstanding=value_test)
        assert stock_test.shares_outstanding == expected_value


if __name__ == "__main__":
    pytest.main([__file__])