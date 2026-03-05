# FinAssistant - Work In Progress

## Current Status: MVP Complete ✓

### Completed Features

#### Backend
- [x] Portfolio model with multi-currency support
- [x] Account model (BANK, BROKERAGE, INSURANCE, PE_PLATFORM)
- [x] Position model with 融资融券 support
- [x] Transaction model for cost basis tracking
- [x] PortfolioSnapshot model for historical tracking
- [x] ImportJob model for screenshot import workflow
- [x] CRUD APIs for all models
- [x] Portfolio summary with metrics (market value, gain/loss, leverage)
- [x] Screenshot upload endpoint
- [x] Vision analysis service (stub - needs LLM integration)
- [x] SQLite database with SQLAlchemy

#### Frontend
- [x] Portfolio list and detail views
- [x] Position table with gain/loss display
- [x] Asset allocation pie chart
- [x] Performance line chart
- [x] Import workflow UI (start, review, confirm)
- [x] Clean light UI theme

#### Infrastructure
- [x] Backend Dockerfile
- [x] Frontend Dockerfile
- [x] docker-compose.yml
- [x] Kubernetes deployment configs
- [x] Ingress configuration

---

## In Progress / TODO

### High Priority

1. **LLM Vision Integration**
   - Integrate MiniMax or OpenAI vision API
   - Connect `/imports/{id}/analyze` to actual vision service
   - Test with real screenshots

2. **Screenshot Import Flow**
   - Link uploaded screenshot to import job
   - Process vision response and save extracted positions
   - Update frontend to handle file upload

3. **Frontend Improvements**
   - Add position edit/delete functionality
   - Add account management UI
   - Improve chart interactivity

### Medium Priority

4. **Price Feed Integration**
   - Implement Yahoo Finance or other data provider
   - Add automatic price updates
   - Cache prices in database

5. **Transaction Features**
   - Add transaction list view
   - Calculate IRR (Internal Rate of Return)
   - Tax lot tracking

6. **Historical Analysis**
   - Better snapshot visualization
   - Compare performance over time
   - Export reports

### Low Priority

7. **Additional Asset Types**
   - Private Equity positions
   - Hedge Fund positions
   - Options/Futures

8. **Advanced Features**
   - Dividend tracking
   - Tax lot optimization
   - Alerts for price movements

---

## Known Issues

1. **MCP Vision** - MiniMax MCP configured but network issues prevent testing
2. **Type Checking** - Some Pydantic type warnings (non-breaking)
3. **Frontend Charts** - Need proper responsive sizing

---

## API Changes Log

### v0.1.0 (Current)
- Initial MVP release
- Portfolio, Account, Position, Transaction models
- Basic CRUD APIs
- Import workflow (stub)
- Docker support

---

## Testing Needed

1. [ ] Create portfolio via UI
2. [ ] Add account to portfolio
3. [ ] Add positions manually
4. [ ] View portfolio summary
5. [ ] Test chart rendering
6. [ ] Upload screenshot
7. [ ] Complete import workflow

---

## Architecture Notes

### Data Flow
```
User Screenshot → Upload → Import Job → Vision API → Review → Confirm → Position
```

### Database Schema
```
Portfolio (1)
  ↘ Account (n)
    ↘ Position (n)
      ↘ Transaction (n)
  ↘ PortfolioSnapshot (n)
  ↘ ImportJob (n)
```

### Multi-Currency
- Each position has `trade_currency` and `exchange_rate`
- Portfolio has `base_currency` for totals
- All values converted to base currency for summary
