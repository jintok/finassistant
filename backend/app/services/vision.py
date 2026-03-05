import json
import os
from typing import List, Dict, Any, Optional
from decimal import Decimal

from app.models.portfolio import AssetType


PROMPT_TEMPLATE = """You are a financial data extraction expert. Analyze this screenshot of a portfolio or stock positions page and extract all positions.

Extract the following information for each position:
- asset_symbol: Stock code/ticker (e.g., "600519", "AAPL", "00700.HK")
- asset_name: Company/stock name
- asset_type: Type of asset (STOCK, ETF, BOND, MUTUAL_FUND, etc.)
- quantity: Number of shares/units
- avg_cost: Average purchase cost per unit (if available)
- current_price: Current market price per unit (if available)
- trade_currency: Currency (CNY, USD, HKD)

Also extract any transactions if visible:
- transaction_type: BUY, SELL, DIVIDEND
- quantity, price, date

Return ONLY a JSON array with no additional text. Format:
[
  {{
    "asset_symbol": "...",
    "asset_name": "...",
    "asset_type": "STOCK",
    "quantity": 100,
    "avg_cost": 150.50,
    "current_price": 180.00,
    "trade_currency": "CNY",
    "confidence": 0.95
  }}
]

If no positions found, return: []"""


def parse_vision_response(response: str) -> List[Dict[str, Any]]:
    try:
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]

        data = json.loads(response.strip())

        normalized = []
        for item in data:
            normalized.append(
                {
                    "asset_symbol": item.get("asset_symbol", ""),
                    "asset_name": item.get("asset_name"),
                    "asset_type": item.get("asset_type", "STOCK"),
                    "quantity": Decimal(str(item.get("quantity", 0))),
                    "avg_cost": Decimal(str(item.get("avg_cost", 0))),
                    "current_price": Decimal(str(item.get("current_price", 0))),
                    "trade_currency": item.get("trade_currency", "CNY"),
                    "confidence": item.get("confidence", 0.8),
                }
            )
        return normalized
    except Exception as e:
        print(f"Error parsing vision response: {e}")
        return []


def get_default_prompt() -> str:
    return PROMPT_TEMPLATE
