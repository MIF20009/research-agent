import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { runsApi, healthApi } from '../api/endpoints';
import toast from 'react-hot-toast';

export const useHealth = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: healthApi.getHealth,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useRuns = (limit?: number) => {
  return useQuery({
    queryKey: ['runs', limit],
    queryFn: () => runsApi.getRuns({ limit }),
    staleTime: 30 * 1000, // 30 seconds
  });
};

export const useRun = (id: number | undefined) => {
  return useQuery({
    queryKey: ['run', id],
    queryFn: () => runsApi.getRun(id!),
    enabled: !!id,
    refetchInterval: (query) => {
      // Poll every 5 seconds if status is running, every 10 seconds if pending, stop when completed/failed
      const status = query.state.data?.status;
      if (status === 'completed' || status === 'failed') return false;
      if (status === 'running') return 5000; // 5 seconds
      return 10000; // 10 seconds for pending/created
    },
  });
};

export const useRunArtifacts = (id: number | undefined) => {
  return useQuery({
    queryKey: ['run-artifacts', id],
    queryFn: () => runsApi.getRunArtifacts(id!),
    enabled: !!id,
    staleTime: 10 * 1000, // 10 seconds
  });
};

export const useCreateRun = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: runsApi.createRun,
    onSuccess: (newRun) => {
      queryClient.invalidateQueries({ queryKey: ['runs'] });
      toast.success('Run created successfully!');
      return newRun;
    },
    onError: (error: Error) => {
      toast.error(error.message);
    },
  });
};

export const useExecuteRun = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: runsApi.executeRun,
    onSuccess: () => {
      toast.success('Run execution started!');
      // Invalidate run and artifacts to trigger refetch
      queryClient.invalidateQueries({ queryKey: ['run'] });
      queryClient.invalidateQueries({ queryKey: ['run-artifacts'] });
    },
    onError: (error: Error) => {
      toast.error(error.message);
    },
  });
};