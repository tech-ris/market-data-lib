from collections.abc import Callable
from abc import ABC, abstractmethod
from typing import Any
import pandas as pd


class Strategy(ABC):
    def __init__(self, name: str):
        """
        name: strategy's identifier
        """
        self.name = name

    @abstractmethod
    def generate_signals(self, prices: pd.Series) -> pd.Series:
        """
        input: asset prices (datetime as index)
        output: position signals (-1,0,1) (datetime as index)
        """
        pass


class StratFactory:
    _registry: dict[str, Callable[..., Strategy]] = {}

    @classmethod
    def register(
        cls, strat_id: str
    ) -> Callable[[Callable[..., Strategy]], Callable[..., Strategy]]:
        def decorator(strat: Callable[..., Strategy]) -> Callable[..., Strategy]:
            cls._registry[strat_id] = strat
            return strat

        return decorator

    @classmethod
    def create(cls, strat_id: str, **kwargs: Any) -> Strategy:
        if strat_id not in cls._registry:
            raise ValueError(f"Unknown: {strat_id}")
        return cls._registry[strat_id](**kwargs)
