import { apiClient } from './client';
import type { Run, Artifact, CreateRunRequest, HealthResponse } from '../types';

export const healthApi = {
  getHealth: (): Promise<HealthResponse> =>
    apiClient.get('/health').then(res => res.data),
};

export const runsApi = {
  createRun: (data: CreateRunRequest): Promise<Run> =>
    apiClient.post('/runs', data).then(res => res.data),

  getRun: (id: number): Promise<Run> =>
    apiClient.get(`/runs/${id}`).then(res => res.data),

  executeRun: (id: number): Promise<void> =>
    apiClient.post(`/runs/${id}/execute`),

  getRunArtifacts: (id: number): Promise<Artifact[]> =>
    apiClient.get(`/runs/${id}/artifacts`).then(res => res.data),

  getRuns: (params?: { limit?: number }): Promise<Run[]> =>
    apiClient.get('/runs', { params }).then(res => res.data),
};