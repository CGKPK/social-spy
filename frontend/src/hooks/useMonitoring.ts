import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { monitoringApi } from '../api/endpoints';

export function useMonitoring() {
  const queryClient = useQueryClient();

  const { data: status, refetch } = useQuery({
    queryKey: ['monitoring-status'],
    queryFn: async () => {
      const response = await monitoringApi.getStatus();
      return response.data;
    },
    refetchInterval: 5000, // Poll every 5 seconds
  });

  const startMutation = useMutation({
    mutationFn: (interval: number) => monitoringApi.start(interval),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['monitoring-status'] });
    },
  });

  const stopMutation = useMutation({
    mutationFn: () => monitoringApi.stop(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['monitoring-status'] });
    },
  });

  const fetchMutation = useMutation({
    mutationFn: () => monitoringApi.fetchNow(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
    },
  });

  return {
    status,
    startMonitoring: startMutation.mutate,
    stopMonitoring: stopMutation.mutate,
    fetchNow: fetchMutation.mutate,
    isStarting: startMutation.isPending,
    isStopping: stopMutation.isPending,
    isFetching: fetchMutation.isPending,
    refetch,
  };
}
