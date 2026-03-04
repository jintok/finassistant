from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional, Dict, List
from datetime import datetime


class PriceFeedInterface(ABC):
    @abstractmethod
    def get_price(self, symbol: str, currency: str = "USD") -> Optional[Decimal]:
        pass

    @abstractmethod
    def get_prices(
        self, symbols: List[str], currency: str = "USD"
    ) -> Dict[str, Decimal]:
        pass


class ManualPriceFeed(PriceFeedInterface):
    def __init__(self):
        self._prices: Dict[str, Decimal] = {}

    def set_price(self, symbol: str, price: Decimal, currency: str = "USD") -> None:
        key = f"{symbol}:{currency}"
        self._prices[key] = price

    def get_price(self, symbol: str, currency: str = "USD") -> Optional[Decimal]:
        key = f"{symbol}:{currency}"
        return self._prices.get(key)

    def get_prices(
        self, symbols: List[str], currency: str = "USD"
    ) -> Dict[str, Decimal]:
        result = {}
        for symbol in symbols:
            price = self.get_price(symbol, currency)
            if price is not None:
                result[symbol] = price
        return result


class YahooFinanceFeed(PriceFeedInterface):
    def __init__(self):
        self._cache: Dict[str, tuple[Decimal, datetime]] = {}
        self._cache_ttl_seconds = 60

    def get_price(self, symbol: str, currency: str = "USD") -> Optional[Decimal]:
        raise NotImplementedError("Yahoo Finance integration not yet implemented")

    def get_prices(
        self, symbols: List[str], currency: str = "USD"
    ) -> Dict[str, Decimal]:
        raise NotImplementedError("Yahoo Finance integration not yet implemented")


price_feed = ManualPriceFeed()
