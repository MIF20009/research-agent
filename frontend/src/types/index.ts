export interface Run {
  id: number;
  topic: string;
  status: string;
  upload_papers: boolean;
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
  upload_papers: boolean;
}

export interface HealthResponse {
  status: string;
}