export interface Run {
  id: number;
  topic: string;
  status: string;
  created_at: string;
}

export interface Artifact {
  id: string;
  kind: string;
  content: string;
  created_at: string;
}

export interface CreateRunRequest {
  topic: string;
}

export interface HealthResponse {
  status: string;
}