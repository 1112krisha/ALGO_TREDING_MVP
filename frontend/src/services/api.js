/**
 * API client for FastAPI backend.
 * In dev: Vite proxies /api → localhost:8000
 * Set VITE_API_URL=http://localhost:8000/api if proxy fails
 */

import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
});

// Better error for backend unreachable
api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (!err.response && err.code === 'ERR_NETWORK') {
      err.message = 'Backend not reachable. Start it with: cd backend && uvicorn app.main:app --port 8000';
    }
    return Promise.reject(err);
  }
);

// Attach JWT to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// No leading slash - axios ignores baseURL when path starts with /
export const auth = {
  register: (email, password) =>
    api.post('auth/register', { email, password }),
  login: (email, password) =>
    api.post('auth/login', { email, password }),
};

export const strategies = {
  create: (data) => api.post('strategies', data),
  list: (activeOnly = false) =>
    api.get('strategies', { params: { active_only: activeOnly } }),
  get: (id) => api.get(`strategies/${id}`),
  start: (id) => api.patch(`strategies/${id}/start`),
  stop: (id) => api.patch(`strategies/${id}/stop`),
};

export const trades = {
  list: (strategyId = null, limit = 100) =>
    api.get('trades', { params: { strategy_id: strategyId, limit } }),
  pnl: (strategyId = null) =>
    api.get('trades/pnl', { params: { strategy_id: strategyId } }),
};

export default api;
