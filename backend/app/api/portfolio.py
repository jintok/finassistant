from datetime import datetime
from typing import List
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db, init_db
from app.models.portfolio import (
    Portfolio,
    Account,
    Position,
    Transaction,
    PortfolioSnapshot,
    ImportJob,
    ImportStatus,
)
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioUpdate,
    PortfolioResponse,
    PortfolioWithAccountsAndPositions,
    AccountCreate,
    AccountUpdate,
    AccountResponse,
    AccountWithPositions,
    PositionCreate,
    PositionUpdate,
    PositionResponse,
    PortfolioSummary,
    TransactionCreate,
    TransactionResponse,
    PortfolioSnapshotCreate,
    PortfolioSnapshotResponse,
    PositionWithTransactions,
    PriceUpdateBatch,
    ImportJobCreate,
    ImportJobUpdate,
    ImportJobResponse,
    ExtractedPosition,
    ExtractedTransaction,
)
from app.services.price_feed import price_feed

router = APIRouter(prefix="/portfolios", tags=["portfolio"])


@router.on_event("startup")
def startup():
    init_db()


@router.post("/", response_model=PortfolioResponse)
def create_portfolio(portfolio: PortfolioCreate, db: Session = Depends(get_db)):
    db_portfolio = Portfolio(
        name=portfolio.name,
        base_currency=portfolio.base_currency,
    )
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


@router.get("/", response_model=List[PortfolioResponse])
def list_portfolios(db: Session = Depends(get_db)):
    return db.query(Portfolio).all()


@router.get("/{portfolio_id}", response_model=PortfolioWithAccountsAndPositions)
def get_portfolio(portfolio_id: str, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


@router.patch("/{portfolio_id}", response_model=PortfolioResponse)
def update_portfolio(
    portfolio_id: str,
    portfolio_update: PortfolioUpdate,
    db: Session = Depends(get_db),
):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    update_data = portfolio_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(portfolio, field, value)

    db.commit()
    db.refresh(portfolio)
    return portfolio


@router.delete("/{portfolio_id}")
def delete_portfolio(portfolio_id: str, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    db.delete(portfolio)
    db.commit()
    return {"message": "Portfolio deleted"}


@router.post("/{portfolio_id}/accounts", response_model=AccountResponse)
def create_account(
    portfolio_id: str,
    account: AccountCreate,
    db: Session = Depends(get_db),
):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    db_account = Account(
        portfolio_id=portfolio_id,
        name=account.name,
        account_type=account.account_type,
        institution=account.institution,
        currency=account.currency,
        external_account_id=account.external_account_id,
        is_margin_enabled=account.is_margin_enabled,
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@router.get("/{portfolio_id}/accounts", response_model=List[AccountResponse])
def list_accounts(portfolio_id: str, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio.accounts


@router.get("/accounts/{account_id}", response_model=AccountWithPositions)
def get_account(account_id: str, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.patch("/accounts/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: str,
    account_update: AccountUpdate,
    db: Session = Depends(get_db),
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    update_data = account_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(account, field, value)

    db.commit()
    db.refresh(account)
    return account


@router.delete("/accounts/{account_id}")
def delete_account(account_id: str, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    db.delete(account)
    db.commit()
    return {"message": "Account deleted"}


@router.post("/accounts/{account_id}/positions", response_model=PositionResponse)
def create_position(
    account_id: str,
    position: PositionCreate,
    db: Session = Depends(get_db),
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    db_position = Position(
        account_id=account_id,
        asset_symbol=position.asset_symbol,
        asset_name=position.asset_name,
        asset_type=position.asset_type,
        quantity=position.quantity,
        avg_cost=position.avg_cost,
        current_price=position.current_price,
        trade_currency=position.trade_currency,
        settlement_currency=position.settlement_currency,
        exchange_rate=position.exchange_rate,
        is_margin_position=position.is_margin_position,
        borrowed_amount=position.borrowed_amount,
        margin_interest_rate=position.margin_interest_rate,
    )
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position


@router.get("/accounts/{account_id}/positions", response_model=List[PositionResponse])
def list_positions(account_id: str, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account.positions


@router.get("/positions/{position_id}", response_model=PositionWithTransactions)
def get_position(position_id: str, db: Session = Depends(get_db)):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position


@router.patch("/positions/{position_id}", response_model=PositionResponse)
def update_position(
    position_id: str,
    position_update: PositionUpdate,
    db: Session = Depends(get_db),
):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    update_data = position_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(position, field, value)

    db.commit()
    db.refresh(position)
    return position


@router.delete("/positions/{position_id}")
def delete_position(position_id: str, db: Session = Depends(get_db)):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    db.delete(position)
    db.commit()
    return {"message": "Position deleted"}


@router.post(
    "/positions/{position_id}/transactions", response_model=TransactionResponse
)
def create_transaction(
    position_id: str,
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    db_transaction = Transaction(
        position_id=position_id,
        transaction_type=transaction.transaction_type,
        quantity=transaction.quantity,
        price_per_unit=transaction.price_per_unit,
        total_amount=transaction.total_amount,
        fee=transaction.fee,
        currency=transaction.currency,
        transaction_date=transaction.transaction_date,
        notes=transaction.notes,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.get(
    "/positions/{position_id}/transactions", response_model=List[TransactionResponse]
)
def list_transactions(position_id: str, db: Session = Depends(get_db)):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position.transactions


@router.get("/{portfolio_id}/summary", response_model=PortfolioSummary)
def get_portfolio_summary(portfolio_id: str, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    total_market_value = Decimal("0")
    total_cost_basis = Decimal("0")
    total_borrowed = Decimal("0")

    for account in portfolio.accounts:
        for position in account.positions:
            qty = Decimal(str(position.quantity))
            price = Decimal(str(position.current_price))
            cost = Decimal(str(position.avg_cost))
            rate = Decimal(str(position.exchange_rate))

            market_value = qty * price * rate
            cost_basis = qty * cost * rate

            total_market_value += market_value
            total_cost_basis += cost_basis

            if position.borrowed_amount:
                total_borrowed += Decimal(str(position.borrowed_amount))

    unrealized_gain = total_market_value - total_cost_basis
    unrealized_gain_pct = (
        (unrealized_gain / total_cost_basis * 100)
        if total_cost_basis > 0
        else Decimal("0")
    )

    leverage_ratio = (
        (total_market_value / (total_market_value - total_borrowed))
        if total_market_value > total_borrowed
        else None
    )

    position_count = sum(len(account.positions) for account in portfolio.accounts)

    return PortfolioSummary(
        portfolio_id=portfolio.id,
        portfolio_name=portfolio.name,
        base_currency=portfolio.base_currency,
        total_market_value=total_market_value,
        total_cost_basis=total_cost_basis,
        unrealized_gain=unrealized_gain,
        unrealized_gain_pct=unrealized_gain_pct,
        total_borrowed_amount=total_borrowed,
        leverage_ratio=leverage_ratio,
        position_count=position_count,
        account_count=len(portfolio.accounts),
    )


@router.post("/{portfolio_id}/snapshots", response_model=PortfolioSnapshotResponse)
def create_snapshot(
    portfolio_id: str,
    snapshot: PortfolioSnapshotCreate,
    db: Session = Depends(get_db),
):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    db_snapshot = PortfolioSnapshot(
        portfolio_id=portfolio_id,
        snapshot_date=snapshot.snapshot_date,
        total_market_value=snapshot.total_market_value,
        total_cost_basis=snapshot.total_cost_basis,
        unrealized_gain=snapshot.unrealized_gain,
        unrealized_gain_pct=snapshot.unrealized_gain_pct,
        total_borrowed_amount=snapshot.total_borrowed_amount,
        leverage_ratio=snapshot.leverage_ratio,
        position_count=snapshot.position_count,
        account_count=snapshot.account_count,
        data=snapshot.data,
    )
    db.add(db_snapshot)
    db.commit()
    db.refresh(db_snapshot)
    return db_snapshot


@router.get("/{portfolio_id}/snapshots", response_model=List[PortfolioSnapshotResponse])
def list_snapshots(portfolio_id: str, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio.snapshots


@router.post("/{portfolio_id}/snapshots/auto", response_model=PortfolioSnapshotResponse)
def create_auto_snapshot(portfolio_id: str, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    total_market_value = Decimal("0")
    total_cost_basis = Decimal("0")
    total_borrowed = Decimal("0")

    for account in portfolio.accounts:
        for position in account.positions:
            qty = Decimal(str(position.quantity))
            price = Decimal(str(position.current_price))
            cost = Decimal(str(position.avg_cost))
            rate = Decimal(str(position.exchange_rate))

            market_value = qty * price * rate
            cost_basis = qty * cost * rate

            total_market_value += market_value
            total_cost_basis += cost_basis

            if position.borrowed_amount:
                total_borrowed += Decimal(str(position.borrowed_amount))

    unrealized_gain = total_market_value - total_cost_basis
    unrealized_gain_pct = (
        (unrealized_gain / total_cost_basis * 100)
        if total_cost_basis > 0
        else Decimal("0")
    )

    leverage_ratio = (
        (total_market_value / (total_market_value - total_borrowed))
        if total_market_value > total_borrowed
        else None
    )

    position_count = sum(len(account.positions) for account in portfolio.accounts)

    db_snapshot = PortfolioSnapshot(
        portfolio_id=portfolio_id,
        snapshot_date=datetime.utcnow(),
        total_market_value=total_market_value,
        total_cost_basis=total_cost_basis,
        unrealized_gain=unrealized_gain,
        unrealized_gain_pct=unrealized_gain_pct,
        total_borrowed_amount=total_borrowed,
        leverage_ratio=leverage_ratio,
        position_count=position_count,
        account_count=len(portfolio.accounts),
    )
    db.add(db_snapshot)
    db.commit()
    db.refresh(db_snapshot)
    return db_snapshot


prices_router = APIRouter(prefix="/prices", tags=["prices"])


@prices_router.post("/update", response_model=dict)
def update_prices(batch: PriceUpdateBatch):
    for price_update in batch.prices:
        price_feed.set_price(
            price_update.symbol, price_update.price, price_update.currency
        )
    return {"message": f"Updated {len(batch.prices)} prices"}


@prices_router.get("/{symbol}", response_model=dict)
def get_price(symbol: str, currency: str = "USD"):
    price = price_feed.get_price(symbol, currency)
    if price is None:
        raise HTTPException(status_code=404, detail="Price not found")
    return {"symbol": symbol, "price": price, "currency": currency}


imports_router = APIRouter(prefix="/imports", tags=["imports"])


@imports_router.post("/start", response_model=ImportJobResponse)
def start_import(
    portfolio_id: str,
    import_data: ImportJobCreate,
    db: Session = Depends(get_db),
):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    db_import = ImportJob(
        portfolio_id=portfolio_id,
        source_type=import_data.source_type,
        status=ImportStatus.PENDING,
    )
    db.add(db_import)
    db.commit()
    db.refresh(db_import)
    return db_import


@imports_router.get("/{import_id}", response_model=ImportJobResponse)
def get_import(import_id: str, db: Session = Depends(get_db)):
    import_job = db.query(ImportJob).filter(ImportJob.id == import_id).first()
    if not import_job:
        raise HTTPException(status_code=404, detail="Import job not found")
    return import_job


@imports_router.patch("/{import_id}/review", response_model=ImportJobResponse)
def review_import(
    import_id: str,
    review_data: ImportJobUpdate,
    db: Session = Depends(get_db),
):
    import_job = db.query(ImportJob).filter(ImportJob.id == import_id).first()
    if not import_job:
        raise HTTPException(status_code=404, detail="Import job not found")

    if import_job.status not in [ImportStatus.REVIEWING, ImportStatus.PENDING]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot review import in {import_job.status} status",
        )

    if review_data.confirmed_positions is not None:
        import_job.confirmed_positions = [
            p.model_dump() for p in review_data.confirmed_positions
        ]
    if review_data.confirmed_transactions is not None:
        import_job.confirmed_transactions = [
            t.model_dump() for t in review_data.confirmed_transactions
        ]
    if review_data.account_mapping is not None:
        import_job.account_mapping = review_data.account_mapping

    import_job.status = ImportStatus.REVIEWING
    db.commit()
    db.refresh(import_job)
    return import_job


@imports_router.post("/{import_id}/confirm", response_model=ImportJobResponse)
def confirm_import(import_id: str, db: Session = Depends(get_db)):
    import_job = db.query(ImportJob).filter(ImportJob.id == import_id).first()
    if not import_job:
        raise HTTPException(status_code=404, detail="Import job not found")

    if import_job.status != ImportStatus.REVIEWING:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot confirm import in {import_job.status} status. Please review first.",
        )

    if not import_job.confirmed_positions and not import_job.confirmed_transactions:
        raise HTTPException(status_code=400, detail="No confirmed data to import")

    portfolio = (
        db.query(Portfolio).filter(Portfolio.id == import_job.portfolio_id).first()
    )
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    account_mapping = import_job.account_mapping or {}
    default_account = None
    if portfolio.accounts:
        default_account = portfolio.accounts[0]
    else:
        default_account = Account(
            portfolio_id=import_job.portfolio_id,
            name=f"{import_job.source_type.value} Account",
            account_type=import_job.source_type.value.replace("雪球", "BROKERAGE")
            .replace("同花顺", "BROKERAGE")
            .replace("招商银行", "BANK")
            if import_job.source_type.value != "MANUAL"
            else "BROKERAGE",
            institution=import_job.source_type.value,
            currency="CNY",
        )
        db.add(default_account)
        db.commit()
        db.refresh(default_account)

    created_positions = []
    created_transactions = []

    for pos_data in import_job.confirmed_positions or []:
        target_account_id = account_mapping.get(
            pos_data.get("asset_symbol", ""), default_account.id
        )
        if not target_account_id:
            target_account_id = default_account.id

        db_position = Position(
            account_id=target_account_id,
            asset_symbol=pos_data.get("asset_symbol", ""),
            asset_name=pos_data.get("asset_name"),
            asset_type=pos_data.get("asset_type", "STOCK"),
            quantity=pos_data.get("quantity", 0),
            avg_cost=pos_data.get("avg_cost", 0),
            current_price=pos_data.get("current_price", 0),
            trade_currency=pos_data.get("trade_currency", "CNY"),
        )
        db.add(db_position)
        created_positions.append(db_position)

    for trans_data in import_job.confirmed_transactions or []:
        target_account_id = account_mapping.get(
            trans_data.get("asset_symbol", ""), default_account.id
        )
        if not target_account_id:
            target_account_id = default_account.id

        positions = (
            db.query(Position)
            .filter(
                Position.account_id == target_account_id,
                Position.asset_symbol == trans_data.get("asset_symbol"),
            )
            .all()
        )
        target_position = positions[0] if positions else None

        if target_position:
            db_transaction = Transaction(
                position_id=target_position.id,
                transaction_type=trans_data.get("transaction_type", "BUY"),
                quantity=trans_data.get("quantity", 0),
                price_per_unit=trans_data.get("price_per_unit", 0),
                total_amount=trans_data.get("total_amount", 0),
                currency=trans_data.get("currency", "CNY"),
                transaction_date=trans_data.get("transaction_date", datetime.utcnow()),
            )
            db.add(db_transaction)
            created_transactions.append(db_transaction)

    import_job.status = ImportStatus.COMPLETED
    db.commit()
    db.refresh(import_job)
    return import_job


@imports_router.delete("/{import_id}")
def cancel_import(import_id: str, db: Session = Depends(get_db)):
    import_job = db.query(ImportJob).filter(ImportJob.id == import_id).first()
    if not import_job:
        raise HTTPException(status_code=404, detail="Import job not found")

    import_job.status = ImportStatus.REJECTED
    db.commit()
    return {"message": "Import cancelled"}


@imports_router.post("/{import_id}/analyze", response_model=ImportJobResponse)
def analyze_import(import_id: str, db: Session = Depends(get_db)):
    import_job = db.query(ImportJob).filter(ImportJob.id == import_id).first()
    if not import_job:
        raise HTTPException(status_code=404, detail="Import job not found")

    if not import_job.screenshot_path:
        raise HTTPException(status_code=400, detail="No screenshot uploaded")

    import_job.status = ImportStatus.ANALYZING
    db.commit()

    return import_job


@router.get("/{portfolio_id}/imports", response_model=List[ImportJobResponse])
def list_imports(portfolio_id: str, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return (
        db.query(ImportJob)
        .filter(ImportJob.portfolio_id == portfolio_id)
        .order_by(ImportJob.created_at.desc())
        .all()
    )
