from market_data_lib.instruments import Instrument

class Portfolio:
    def __init__(self, positions: dict[Instrument, float]) -> None:
        self._positions = positions

    @property
    def positions(self) -> dict[Instrument, float]:
        return self._positions
    
    @property
    def assets(self) -> set[str]:
        return {instrument.ticker for instrument in self.positions.keys()}

    def __repr__(self) -> str:
        return f"{self.positions}"

    def __str__(self) -> str:
        tickers_qties = {instrument.ticker: qty for instrument, qty in self.positions.items()}
        return f"Portfolio({tickers_qties})"

    def add_position(self, instrument: Instrument, quantity: float) -> None:
        if quantity <= 0: raise ValueError("The quantity added must be positive")
        current_qty: float = 0 if instrument not in self.positions else self.positions[instrument] #self.positions.get(instrument) if instrument in self.positions else 0
        self.positions.update({instrument : current_qty + quantity})

    def remove_position(self, instrument: Instrument, quantity: float | None = None) -> None:
        if instrument not in self.positions: # ValueError if the instrument is not in the portfolio
            raise ValueError(f"{instrument.ticker} is not in the portfolio.")
        if quantity == None:    # full removal of the position if no quantity is indicated
            del self.positions[instrument]
            return
        new_qty: float = self.positions[instrument] - quantity
        if new_qty < 0:     # ValueError if the quantity to be removed > existing quantity
            raise ValueError(f"Cannot remove more than the current number of positions ({self.positions.get(instrument)}) for this security")
        if new_qty == 0:    # removal if the quantity hit 0 
            del self.positions[instrument]
        else:
            self.positions.update({instrument : new_qty})

    def quantity(self, instrument: Instrument) -> float:
        qty = self.positions[instrument]
        return qty

    def number_assets(self) -> float:
        total_qty = sum([qty for qty in self.positions.values()])
        return total_qty

    def weight(self, instrument: Instrument) -> float:
        total_qty = sum([qty for qty in self.positions.values()])
        instrument_qty = self.positions[instrument] / total_qty
        return round(instrument_qty, 4)

    def weights(self) -> dict[str, float]:
        total_qty = sum([qty for qty in self.positions.values()])
        return {instrument.ticker : round(qty / total_qty, 4) for instrument, qty in self.positions.items()}

    def value_asset(self, instrument: Instrument) -> float | NotImplementedError:
        if instrument not in self.positions: 
            raise ValueError(f"{instrument.ticker} is not in the portfolio")
        if not isinstance(instrument.price(), (int, float)):
            raise NotImplementedError("No price defined for this asset")
        return instrument.price()

    def value_position(self, instrument: Instrument) -> float | str:
        if instrument not in self.positions:
            raise ValueError(f"{instrument.ticker} is not in the portfolio")
        instrument_price = instrument.price()       # mypy-compliant, allow mypy checking (strict mode)
        if isinstance(instrument_price, NotImplementedError):
            raise NotImplementedError("No price defined for this asset")
        else:
            return instrument_price * self.positions[instrument]
    
    def total_value(self) -> float:
        non_priced_securities = []
        price = 0.0
        for instrument, quantity in self.positions.items():
            instrument_price = instrument.price()
            if isinstance(instrument_price, NotImplementedError):
                non_priced_securities.append(instrument.ticker)
            else:
                price += quantity * instrument_price 
        if non_priced_securities != []: 
            print(f"[PRICE NOT DEFINED] The value displayed do not include the following asset(s): {", ".join(non_priced_securities)}")
        return price