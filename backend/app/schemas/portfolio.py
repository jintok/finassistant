from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Any
from pydantic import BaseModel, Field

from app.models.portfolio import AccountType, AssetType, TransactionType


class PortfolioBase(BaseModel):
    name: str
    base_currency: str = "CNY"


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    base_currency: Optional[str] = None


class PortfolioResponse(PortfolioBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AccountBase(BaseModel):
    name: str
    account_type: AccountType
    institution: str
    currency: str
    external_account_id: Optional[str] = None
    is_margin_enabled: bool = False


class AccountCreate(AccountBase):
    portfolio_id: str


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    account_type: Optional[AccountType] = None
    institution: Optional[str] = None
    currency: Optional[str] = None
    external_account_id: Optional[str] = None
    is_margin_enabled: Optional[bool] = None


class AccountResponse(AccountBase):
    id: str
    portfolio_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PositionBase(BaseModel):
    asset_symbol: str
    asset_name: Optional[str] = None
    asset_type: AssetType
    quantity: Decimal = Field(default=0, decimal_places=8)
    avg_cost: Decimal = Field(default=0, decimal_places=8)
    current_price: Decimal = Field(default=0, decimal_places=8)
    trade_currency: str
    settlement_currency: Optional[str] = None
    exchange_rate: Decimal = Field(default=1, decimal_places=8)
    is_margin_position: bool = False
    borrowed_amount: Optional[Decimal] = Field(default=None, decimal_places=8)
    margin_interest_rate: Optional[Decimal] = Field(default=None, decimal_places=6)


class PositionCreate(PositionBase):
    account_id: str


class PositionUpdate(BaseModel):
    asset_name: Optional[str] = None
    quantity: Optional[Decimal] = None
    avg_cost: Optional[Decimal] = None
    current_price: Optional[Decimal] = None
    trade_currency: Optional[str] = None
    settlement_currency: Optional[str] = None
    exchange_rate: Optional[Decimal] = None
    is_margin_position: Optional[bool] = None
    borrowed_amount: Optional[Decimal] = None
    margin_interest_rate: Optional[Decimal] = None


class PositionResponse(PositionBase):
    id: str
    account_id: str
    last_updated: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class PortfolioWithDetails(PortfolioResponse):
    accounts: List[AccountResponse] = []


class AccountWithPositions(AccountResponse):
    positions: List[PositionResponse] = []


class PortfolioWithAccountsAndPositions(PortfolioResponse):
    accounts: List[AccountWithPositions] = []


class PositionSummary(BaseModel):
    total_market_value: Decimal = Field(default=0, decimal_places=8)
    total_cost_basis: Decimal = Field(default=0, decimal_places=8)
    unrealized_gain: Decimal = Field(default=0, decimal_places=8)
    unrealized_gain_pct: Decimal = Field(default=0, decimal_places=4)


class PortfolioSummary(BaseModel):
    portfolio_id: str
    portfolio_name: str
    base_currency: str
    total_market_value: Decimal = Field(default=0, decimal_places=8)
    total_cost_basis: Decimal = Field(default=0, decimal_places=8)
    unrealized_gain: Decimal = Field(default=0, decimal_places=8)
    unrealized_gain_pct: Decimal = Field(default=0, decimal_places=4)
    total_borrowed_amount: Decimal = Field(default=0, decimal_places=8)
    leverage_ratio: Optional[Decimal] = Field(default=None, decimal_places=4)
    position_count: int = 0
    account_count: int = 0


class TransactionBase(BaseModel):
    transaction_type: TransactionType
    quantity: Decimal = Field(default=0, decimal_places=8)
    price_per_unit: Decimal = Field(default=0, decimal_places=8)
    total_amount: Decimal = Field(default=0, decimal_places=8)
    fee: Decimal = Field(default=0, decimal_places=8)
    currency: str
    transaction_date: datetime
    notes: Optional[str] = None


class TransactionCreate(TransactionBase):
    position_id: str


class TransactionUpdate(BaseModel):
    quantity: Optional[Decimal] = None
    price_per_unit: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    fee: Optional[Decimal] = None
    transaction_date: Optional[datetime] = None
    notes: Optional[str] = None


class TransactionResponse(TransactionBase):
    id: str
    position_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class PortfolioSnapshotBase(BaseModel):
    snapshot_date: datetime
    total_market_value: Decimal = Field(default=0, decimal_places=8)
    total_cost_basis: Decimal = Field(default=0, decimal_places=8)
    unrealized_gain: Decimal = Field(default=0, decimal_places=8)
    unrealized_gain_pct: Decimal = Field(default=0, decimal_places=4)
    total_borrowed_amount: Decimal = Field(default=0, decimal_places=8)
    leverage_ratio: Optional[Decimal] = Field(default=None, decimal_places=4)
    position_count: int = 0
    account_count: int = 0
    data: Optional[Any] = None


class PortfolioSnapshotCreate(PortfolioSnapshotBase):
    portfolio_id: str


class PortfolioSnapshotResponse(PortfolioSnapshotBase):
    id: str
    portfolio_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class PositionWithTransactions(PositionResponse):
    transactions: List[TransactionResponse] = []


class PriceUpdate(BaseModel):
    symbol: str
    price: Decimal
    currency: str = "USD"


class PriceUpdateBatch(BaseModel):
    prices: List[PriceUpdate]
