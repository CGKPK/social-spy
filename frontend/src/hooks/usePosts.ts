import { useQuery } from '@tanstack/react-query';
import { postsApi } from '../api/endpoints';

export function usePosts(filters?: {
  platform?: string;
  type?: string;
  author?: string;
  limit?: number;
  offset?: number;
}) {
  return useQuery({
    queryKey: ['posts', filters],
    queryFn: async () => {
      const response = await postsApi.getPosts(filters);
      return response.data;
    },
  });
}

export function useStats() {
  return useQuery({
    queryKey: ['stats'],
    queryFn: async () => {
      const response = await postsApi.getStats();
      return response.data;
    },
    refetchInterval: 30000, // Refresh every 30 seconds
  });
}
