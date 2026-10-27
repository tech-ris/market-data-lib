from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    def __init__(self, name: str):
        """
        Initializes the strategy with a name as identifier.
        """
        self.name = name
        pass

    @abstractmethod
    def generate_signals(self, prices: pd.Series) -> pd.Series:
        """
        Abstract method to be implemented by all subclasses.
        
        parameter:
        prices: a time-series of asset prices (Index: DatetimeIndex, Values: float)
            
        returns:
        signals: a time-series of position signals aligned with the input index.
        """
        pass