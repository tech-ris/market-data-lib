from datetime import date
from contextlib import nullcontext
import pytest


# Instrument
## Initial tests: default behavior tests
def test_instrument_default_values(default_equity):
    instrument = default_equity(ticker="INSTR")
    assert instrument.ticker == "INSTR"
    assert instrument.currency == "CUR"


## Ticker
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context",
    [
        pytest.param("  I N   S  TR  ", "INSTR", nullcontext(), id="Handle Whitespace"),
        pytest.param(
            "  ",
            None,
            pytest.raises(ValueError, match="^Missing ticker$"),
            id="No Empty ticker",
        ),
    ],
)
def test_instrument_ticker(
    default_equity, value_test, expected_value, expected_context
):
    with expected_context:
        instrument = default_equity(ticker=value_test)
        assert instrument.ticker == expected_value


## Currency
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context",
    [
        pytest.param(
            "  C     UR  ",
            "CUR",
            nullcontext(),
            id="Handle Whitespace",
        ),
        pytest.param(
            "  ",
            None,
            pytest.raises(ValueError, match="^Missing currency"),
            id="No empty ticker",
        ),
        pytest.param(
            "C0R",
            None,
            pytest.raises(ValueError, match="^Currency must have three letters$"),
            id="Letters only",
        ),
        pytest.param(
            "CU",
            None,
            pytest.raises(ValueError, match="^Currency must have three letters$"),
            id="No less than three letters",
        ),
        pytest.param(
            "CURR",
            None,
            pytest.raises(ValueError, match="^Currency must have three letters$"),
            id="No more than three letters",
        ),
    ],
)
def test_instrument_currency(
    default_equity, value_test, expected_value, expected_context
):
    with expected_context:
        instrument = default_equity(currency=value_test)
        assert instrument.currency == expected_value


# Equity
## Initial tests: default behavior tests
def test_equity_default_values(default_equity):
    stock = default_equity()
    assert stock.adj_price == 150
    assert stock.shares_outstanding == 400_000
    assert stock.price() == 150
    assert stock.market_cap == 150 * 400_000


## Adjusted Closing Price
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context",
    [
        pytest.param(
            0,
            None,
            pytest.raises(ValueError, match="^Stock price must be positive$"),
            id="No null adjusted close price",
        ),
        pytest.param(
            -1,
            None,
            pytest.raises(ValueError, match="^Stock price must be positive$"),
            id="No negative adjusted close price",
        ),
    ],
)
def test_equity_adj_price(default_equity, value_test, expected_value, expected_context):
    with expected_context:
        stock = default_equity(adj_price=value_test)
        assert stock.adj_price == expected_value


## Number of Outstanding Shares
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context",
    [
        pytest.param(
            -1,
            None,
            pytest.raises(
                ValueError, match="^Number of outstanding shares must be positive$"
            ),
            id="No negative outstanding shares",
        )
    ],
)
def test_equity_shares_outstanding(
    default_equity, value_test, expected_value, expected_context
):
    with expected_context:
        stock = default_equity(shares_outstanding=value_test)
        assert stock.shares_outstanding == expected_value


## Market Cap
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context",
    [
        pytest.param(
            None,
            None,
            pytest.raises(ValueError, match="[shares_outstanding = None]"),
            id="No outstd shares --> no market cap",
        )
    ],
)
def test_equity_market_cap(
    default_equity, value_test, expected_value, expected_context
):
    stock = default_equity(shares_outstanding=value_test)
    with expected_context:
        assert stock.market_cap == expected_value


# Bond
## Initial tests: default behavior tests
def test_default_values_bond(default_bond):
    bond = default_bond()
    assert bond.face_value == 1000
    assert bond.coupon_rate == 0.05
    assert bond.years_to_maturity == 10
    assert bond.market_price == 98.72
    assert bond.price() == 1000 * 98.72 / 100
    assert bond.ytm == round(
        (0.05 * 1000 + (1000 - 987.20) / 10) / ((1000 + 987.20) / 2), 4
    )


## Face Value
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context",
    [
        pytest.param(
            0,
            None,
            pytest.raises(ValueError, match="^Bond's face value must be positive$"),
            id="No null face value",
        ),
        pytest.param(
            -1,
            None,
            pytest.raises(ValueError, match="^Bond's face value must be positive$"),
            id="No negative face value",
        ),
    ],
)
def test_bond_face_value(default_bond, value_test, expected_value, expected_context):
    with expected_context:
        bond = default_bond(face_value=value_test)
        assert bond.face_value == expected_value


## Coupon Rate
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context",
    [
        pytest.param(
            0,
            None,
            pytest.raises(ValueError, match="^Bond's coupon rate must be positive$"),
            id="No null coupon rate",
        ),
        pytest.param(
            -1,
            None,
            pytest.raises(ValueError, match="^Bond's coupon rate must be positive$"),
            id="No negative coupon rate",
        ),
    ],
)
def test_bond_coupon_rate(default_bond, value_test, expected_value, expected_context):
    with expected_context:
        bond = default_bond(coupon_rate=value_test)
        assert bond.coupon_rate == expected_value


## Maturity
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context",
    [
        pytest.param(
            0,
            None,
            pytest.raises(
                ValueError, match="^Bond's years to maturity must be positive$"
            ),
            id="No null years to maturity",
        ),
        pytest.param(
            -1,
            None,
            pytest.raises(
                ValueError, match="^Bond's years to maturity must be positive$"
            ),
            id="No negative years to maturity",
        ),
    ],
)
def test_bond_years_to_maturity(
    default_bond, value_test, expected_value, expected_context
):
    with expected_context:
        bond = default_bond(years_to_maturity=value_test)
        assert bond.years_to_maturity == expected_value


## Market Price
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context",
    [
        pytest.param(
            0,
            None,
            pytest.raises(ValueError, match="^Bond's market price must be positive$"),
            id="No null market price",
        ),
        pytest.param(
            -1,
            None,
            pytest.raises(ValueError, match="^Bond's market price must be positive$"),
            id="No negative market price",
        ),
    ],
)
def test_bond_market_price(default_bond, value_test, expected_value, expected_context):
    with expected_context:
        bond = default_bond(market_price=value_test)
        assert bond.market_price == expected_value


# Option
## Initial tests: default behavior tests
def test_default_values_option(default_option, default_equity):
    option = default_option()
    assert option.underlying == default_equity()
    assert option.option_type == "Call"
    assert option.strike == 175
    assert option.expiry == date(2027, 12, 31)


## Underlying
def test_option_underlying(default_option):
    """Test if TypeError raise when underlying is not an Equity object"""
    with pytest.raises(TypeError, match="^The underlying must be an Equity object$"):
        option = default_option(underlying="Equity")
        assert option.underlying == None


## Option Type
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context",
    [
        pytest.param(
            "  c  A l   L ",
            "Call",
            nullcontext(),
            id="Handle whitespace",
        ),
        pytest.param(
            "c ",
            "Call",
            nullcontext(),
            id="Ok with single letter for call",
        ),
        pytest.param(
            " p",
            "Put",
            nullcontext(),
            id="Ok with single letter for put",
        ),
        pytest.param(
            "",
            None,
            pytest.raises(ValueError, match="Must be either call "),
            id="No empty option type",
        ),
        pytest.param(
            "Calll",
            None,
            pytest.raises(ValueError, match="Must be either call "),
            id="No non existing option type",
        ),
    ],
)
def test_option_option_type(
    default_option, value_test, expected_value, expected_context
):
    with expected_context:
        option = default_option(option_type=value_test)
        assert option.option_type == expected_value


## Strike
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context",
    [
        pytest.param(
            0,
            None,
            pytest.raises(ValueError, match="^Strike price must be positive$"),
            id="Null strike price",
        ),
        pytest.param(
            -1,
            None,
            pytest.raises(ValueError, match="^Strike price must be positive$"),
            id="Negative strike price",
        ),
    ],
)
def test_option_strike(default_option, value_test, expected_value, expected_context):
    with expected_context:
        option = default_option(strike=value_test)
        assert option.strike == expected_value


if __name__ == "__main__":
    pytest.main([__file__])
