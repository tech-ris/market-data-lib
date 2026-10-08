import pytest


def test_portfolio_default(default_pf, default_equity, default_bond):
    def_eq, def_bnd = default_equity(), default_bond()
    pf = default_pf()
    assert pf.positions == {def_eq: 10, def_bnd: 2}
    assert pf.assets == {def_eq.ticker, def_bnd.ticker}
    assert pf.quantity(def_eq) == 10
    assert pf.number_assets() == 10 + 2
    assert pf.weight(def_eq) == round(10 / 12, 4)
    assert pf.weights() == {
        def_eq.ticker: round(10 / 12, 4),
        def_bnd.ticker: round(2 / 12, 4),
    }
    assert pf.value_asset(def_eq) == 150
    assert pf.value_position(def_eq) == 150 * 10
    assert pf.total_value() == 150 * 10 + 987.2 * 2


def test_portfolio_w_option_default(
    default_pf, default_equity, default_bond, default_option
):
    def_eq, def_bnd = default_equity(), default_bond()
    def_opt = default_option()
    pf = default_pf((def_opt, 7))  # Test with options
    assert pf.positions == {def_eq: 10, def_bnd: 2, def_opt: 7}

    with pytest.raises(match="^No price defined for this asset$"):
        assert pf.value_asset(def_opt) == None
        assert pf.value_position(def_opt) == None

    assert pf.total_value() == 150 * 10 + 987.2 * 2


if __name__ == "__main__":
    pytest.main([__file__])
