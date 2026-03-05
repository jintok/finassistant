import axios from 'axios';

const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000',
});

export default {
  getPortfolios() {
    return api.get('/portfolios/');
  },
  
  getPortfolio(id) {
    return api.get(`/portfolios/${id}`);
  },
  
  createPortfolio(data) {
    return api.post('/portfolios/', data);
  },
  
  getPortfolioSummary(id) {
    return api.get(`/portfolios/${id}/summary`);
  },
  
  getAccounts(portfolioId) {
    return api.get(`/portfolios/${portfolioId}/accounts`);
  },
  
  createAccount(portfolioId, data) {
    return api.post(`/portfolios/${portfolioId}/accounts`, data);
  },
  
  getPositions(accountId) {
    return api.get(`/portfolios/accounts/${accountId}/positions`);
  },
  
  createPosition(accountId, data) {
    return api.post(`/portfolios/accounts/${accountId}/positions`, data);
  },
  
  updatePosition(positionId, data) {
    return api.patch(`/portfolios/positions/${positionId}`, data);
  },
  
  deletePosition(positionId) {
    return api.delete(`/portfolios/positions/${positionId}`);
  },
  
  getTransactions(positionId) {
    return api.get(`/portfolios/positions/${positionId}/transactions`);
  },
  
  createTransaction(positionId, data) {
    return api.post(`/portfolios/positions/${positionId}/transactions`, data);
  },
  
  getSnapshots(portfolioId) {
    return api.get(`/portfolios/${portfolioId}/snapshots`);
  },
  
  createSnapshot(portfolioId) {
    return api.post(`/portfolios/${portfolioId}/snapshots/auto`);
  },
  
  getImports(portfolioId) {
    return api.get(`/portfolios/${portfolioId}/imports`);
  },
  
  startImport(portfolioId, data) {
    return api.post(`/imports/start?portfolio_id=${portfolioId}`, data);
  },
  
  getImport(importId) {
    return api.get(`/imports/${importId}`);
  },
  
  reviewImport(importId, data) {
    return api.patch(`/imports/${importId}/review`, data);
  },
  
  confirmImport(importId) {
    return api.post(`/imports/${importId}/confirm`);
  },
  
  cancelImport(importId) {
    return api.delete(`/imports/${importId}`);
  },
  
  updatePrices(data) {
    return api.post('/prices/update', data);
  },
  
  getPrice(symbol) {
    return api.get(`/prices/${symbol}`);
  },
};
