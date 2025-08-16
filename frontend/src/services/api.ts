import axios from 'axios';
import { InsightRequest, InsightResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 minutes timeout for scraping
  headers: {
    'Content-Type': 'application/json',
  },
});

export const insightsApi = {
  /**
   * Fetch insights from a Shopify store
   */
  async getInsights(request: InsightRequest): Promise<InsightResponse> {
    try {
      const response = await api.post<InsightResponse>('/api/insights', request);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response) {
          // Server responded with error status
          throw new Error(error.response.data?.detail || error.response.data?.error || 'Request failed');
        } else if (error.request) {
          // Request was made but no response received
          throw new Error('No response from server. Please check your connection.');
        } else {
          // Something else happened
          throw new Error(error.message || 'An error occurred');
        }
      }
      throw error;
    }
  },

  /**
   * Validate if a URL is a Shopify store
   */
  async validateUrl(url: string): Promise<{ url: string; is_shopify_store: boolean; valid: boolean }> {
    try {
      const response = await api.get('/api/validate-url', {
        params: { url }
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response) {
          throw new Error(error.response.data?.detail || 'Validation failed');
        } else if (error.request) {
          throw new Error('No response from server');
        } else {
          throw new Error(error.message || 'Validation error');
        }
      }
      throw error;
    }
  },

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string; timestamp: number }> {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('Health check failed');
    }
  }
};

export default api;
