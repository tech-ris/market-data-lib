from contextlib import nullcontext
import pytest


# Default Portfolio
def test_portfolio_default(default_pf, default_equity, default_bond, default_option):
    def_eq, def_bnd = default_equity(), default_bond()
    pf = default_pf()
    assert pf.positions == {def_eq: 10, def_bnd: 2}
    assert pf.__repr__() == "{" + f"{def_eq}: 10, {def_bnd}: 2" + "}"
    assert pf.assets == {def_eq.ticker, def_bnd.ticker}
    assert pf.__str__() == "{'STCK': 10, 'BND': 2}"
    assert pf.quantity(def_eq) == 10
    with pytest.raises(KeyError):
        assert pf.quantity(default_equity(ticker="STCK2"))
    assert pf.number_assets() == 10 + 2
    assert pf.weight(def_eq) == round(10 / 12, 4)
    assert pf.weights() == {
        def_eq.ticker: round(10 / 12, 4),
        def_bnd.ticker: round(2 / 12, 4),
    }
    assert pf.value_asset(def_eq) == 150
    with pytest.raises(KeyError):
        assert pf.value_asset(default_equity(ticker="STCK2"))
    assert pf.value_position(def_eq) == 150 * 10
    with pytest.raises(KeyError):
        assert pf.value_position(default_equity(ticker="STCK2"))
    assert pf.total_value() == 150 * 10 + 987.2 * 2

    # Tests with instrument without price()
    def_opt = default_option()
    pf = default_pf({def_opt: 7})
    assert pf.positions == {def_eq: 10, def_bnd: 2, def_opt: 7}
    assert pf.total_value() == 150 * 10 + 987.2 * 2
    with pytest.raises(match="^No price defined for this asset$"):
        pf.value_asset(def_opt)
    with pytest.raises(match="^No price defined for this asset$"):
        pf.value_position(def_opt)


# Add position
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context",
    [
        pytest.param(
            -1,
            None,
            pytest.raises(ValueError, match="^The quantity added must be positive$"),
            id="No neagtive added quantity",
        ),
        pytest.param(
            0,
            None,
            pytest.raises(ValueError, match="^The quantity added must be positive$"),
            id="No null added quantity",
        ),
        pytest.param(2, 12, nullcontext(), id="Normal case"),
    ],
)
def test_portfolio_add_position(
    default_pf, default_equity, value_test, expected_value, expected_context
):
    pf = default_pf()
    with expected_context:
        pf.add_position(default_equity(), value_test)
        assert pf.quantity(default_equity()) == expected_value


def test_portfolio_add_position_new_instrument(default_pf, default_option, quantity=5):
    pf = default_pf()
    pf.add_position(default_option, quantity)
    assert pf.quantity(default_option) == 5


# Remove position
@pytest.mark.parametrize(
    "value_test, expected_value, expected_context",
    [
        pytest.param(
            -1,
            None,
            pytest.raises(ValueError, match="^The quantity removed must be positive$"),
            id="No neagtive removed quantity",
        ),
        pytest.param(
            0,
            None,
            pytest.raises(ValueError, match="^The quantity removed must be positive$"),
            id="No null removed quantity",
        ),
        pytest.param(
            12,
            None,
            pytest.raises(
                ValueError,
                match="^Cannot remove more than the instrument's quantity",
            ),
            id="Removed quantity > Current quantity",
        ),
        pytest.param(3, 7, nullcontext(), id="Normal case"),
        pytest.param(
            None, None, pytest.raises(KeyError), id="Asset removed"
        ),  # KeyError in pf.quantity(instrument) as asset removed (case new_qty == 0)
    ],
)
def test_portfolio_remove_position(
    default_pf, default_equity, value_test, expected_value, expected_context
):
    pf = default_pf()
    with expected_context:
        pf.remove_position(default_equity(), value_test)
        assert pf.quantity(default_equity()) == expected_value


if __name__ == "__main__":
    pytest.main([__file__])
