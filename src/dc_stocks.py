from dataclasses import dataclass


@dataclass
class Stock:
    symbol: str
    current: float
    high: float
    low: float



@dataclass
class StockDefaults:
    name: str
    current: float = 0.0
    high: float = 0.0
    low: float = 0.0




@dataclass(order=True)
class StockOrdered:
    name: str
    current: float = 0.0
    high: float = 0.0
    low: float = 0.0


