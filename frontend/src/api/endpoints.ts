import { apiClient } from './client';

export const monitoringApi = {
  getStatus: () => apiClient.get('/monitoring/status'),
  start: (interval_minutes: number) =>
    apiClient.post('/monitoring/start', { interval_minutes }),
  stop: () => apiClient.post('/monitoring/stop'),
  fetchNow: () => apiClient.post('/monitoring/fetch'),
};

export const postsApi = {
  getPosts: (filters?: {
    platform?: string;
    type?: string;
    author?: string;
    limit?: number;
    offset?: number;
  }) => apiClient.get('/posts', { params: filters }),
  getStats: () => apiClient.get('/posts/stats'),
  getRecent: (days = 7, limit = 50) =>
    apiClient.get('/posts/recent', { params: { days, limit } }),
};

export const configApi = {
  getConfig: () => apiClient.get('/config'),
  updateKeywords: (keywords: string[]) =>
    apiClient.put('/config/keywords', { keywords }),
  updateYouTubeChannels: (channels: { name: string; channel_id: string }[]) =>
    apiClient.put('/config/channels/youtube', { channels }),
  updateTwitterAccounts: (accounts: string[]) =>
    apiClient.put('/config/accounts/twitter', { accounts }),
};

export const manualApi = {
  getEntries: () => apiClient.get('/manual'),
  createEntry: (entry: {
    platform: string;
    text: string;
    author?: string;
    url?: string;
    tags?: string[];
  }) => apiClient.post('/manual', entry),
  deleteEntry: (id: string) => apiClient.delete(`/manual/${id}`),
};

export const reportsApi = {
  generateDashboard: () => apiClient.post('/reports/dashboard'),
  generateTrends: () => apiClient.post('/reports/trends'),
  getDashboardData: () => apiClient.get('/reports/dashboard/data'),
};
