import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Numeric,
    ForeignKey,
    Enum,
    JSON,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class AccountType(str, PyEnum):
    BANK = "BANK"
    BROKERAGE = "BROKERAGE"
    INSURANCE = "INSURANCE"
    PE_PLATFORM = "PE_PLATFORM"


class AssetType(str, PyEnum):
    STOCK = "STOCK"
    ETF = "ETF"
    BOND = "BOND"
    MUTUAL_FUND = "MUTUAL_FUND"
    MONEY_MARKET = "MONEY_MARKET"
    DEPOSIT = "DEPOSIT"


class TransactionType(str, PyEnum):
    BUY = "BUY"
    SELL = "SELL"
    DIVIDEND = "DIVIDEND"
    INTEREST = "INTEREST"
    FEE = "FEE"
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    base_currency = Column(String, default="CNY")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    accounts = relationship(
        "Account", back_populates="portfolio", cascade="all, delete-orphan"
    )
    snapshots = relationship(
        "PortfolioSnapshot", back_populates="portfolio", cascade="all, delete-orphan"
    )


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String, ForeignKey("portfolios.id"), nullable=False)
    name = Column(String, nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    institution = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    external_account_id = Column(String, nullable=True)
    is_margin_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    portfolio = relationship("Portfolio", back_populates="accounts")
    positions = relationship(
        "Position", back_populates="account", cascade="all, delete-orphan"
    )


class Position(Base):
    __tablename__ = "positions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    asset_symbol = Column(String, nullable=False)
    asset_name = Column(String, nullable=True)
    asset_type = Column(Enum(AssetType), nullable=False)
    quantity = Column(Numeric(18, 8), default=0)
    avg_cost = Column(Numeric(18, 8), default=0)
    current_price = Column(Numeric(18, 8), default=0)
    trade_currency = Column(String, nullable=False)
    settlement_currency = Column(String, nullable=True)
    exchange_rate = Column(Numeric(18, 8), default=1)
    is_margin_position = Column(Boolean, default=False)
    borrowed_amount = Column(Numeric(18, 8), nullable=True)
    margin_interest_rate = Column(Numeric(10, 6), nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="positions")
    transactions = relationship(
        "Transaction", back_populates="position", cascade="all, delete-orphan"
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    position_id = Column(String, ForeignKey("positions.id"), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Numeric(18, 8), default=0)
    price_per_unit = Column(Numeric(18, 8), default=0)
    total_amount = Column(Numeric(18, 8), default=0)
    fee = Column(Numeric(18, 8), default=0)
    currency = Column(String, nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    position = relationship("Position", back_populates="transactions")


class ImportStatus(str, PyEnum):
    PENDING = "PENDING"
    ANALYZING = "ANALYZING"
    REVIEWING = "REVIEWING"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


class SourceType(str, PyEnum):
    XUEQIU = "雪球"
    TONGHUASHUN = "同花顺"
    ZHAOSHANG = "招商银行"
    MANUAL = "MANUAL"


class PortfolioSnapshot(Base):
    __tablename__ = "portfolio_snapshots"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String, ForeignKey("portfolios.id"), nullable=False)
    snapshot_date = Column(DateTime, nullable=False)
    total_market_value = Column(Numeric(18, 8), default=0)
    total_cost_basis = Column(Numeric(18, 8), default=0)
    unrealized_gain = Column(Numeric(18, 8), default=0)
    unrealized_gain_pct = Column(Numeric(10, 4), default=0)
    total_borrowed_amount = Column(Numeric(18, 8), default=0)
    leverage_ratio = Column(Numeric(10, 4), nullable=True)
    position_count = Column(Numeric(10, 0), default=0)
    account_count = Column(Numeric(10, 0), default=0)
    data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    portfolio = relationship("Portfolio", back_populates="snapshots")


class ImportJob(Base):
    __tablename__ = "import_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String, ForeignKey("portfolios.id"), nullable=False)
    status = Column(Enum(ImportStatus), default=ImportStatus.PENDING)
    source_type = Column(Enum(SourceType), nullable=False)
    screenshot_path = Column(String, nullable=True)
    extracted_positions = Column(JSON, nullable=True)
    extracted_transactions = Column(JSON, nullable=True)
    confirmed_positions = Column(JSON, nullable=True)
    confirmed_transactions = Column(JSON, nullable=True)
    account_mapping = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
