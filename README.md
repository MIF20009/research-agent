# 🧠 Multi-Agent Research Assistant  
**Agentic AI System for Automated Literature Review**

---

## 📌 Overview

This project is a **dockerized, agent-based AI system** designed to **automate literature reviews** using **Large Language Models (LLMs)** and a **multi-agent workflow**.

It supports the full pipeline from:
- topic input
- paper retrieval
- information extraction
- synthesis & gap analysis
- hypothesis generation  

All results are **persisted, cached, and reusable**, making the system efficient, scalable, and cost-controlled.

The system is suitable for:
- academic research assistance
- AI agent coursework (Agentic AI)
- research automation products

---

## 🎯 Key Features

### ✅ Multi-Agent Architecture
- Each research step is handled by a **specialized agent**
- Agents communicate through a **shared graph state**
- Implemented using **LangGraph**

### ✅ Automated Literature Review
- Retrieves papers from **OpenAlex**
- Extracts structured knowledge (problem, method, results, limitations)
- Produces:
  - literature synthesis
  - research gaps
  - testable hypotheses

### ✅ Persistent Research Runs
- Each run is tracked with status:
  - `pending → running → completed / failed`
- All outputs are stored in PostgreSQL

### ✅ Caching & Cost Control
- **Retrieval cache** avoids re-querying OpenAlex for the same topic
- **Embeddings cache** prevents re-embedding identical texts
- Reduces:
  - API usage
  - runtime
  - OpenAI cost

### ✅ Fully Dockerized
- No local Python or Postgres setup required
- One-command startup
- Reproducible across machines

### ✅ API-First (FastAPI)
- Swagger UI automatically available
- Easy future frontend integration

---

## 🏗️ System Architecture

### Services
| Service | Description |
|------|------------|
| `api` | FastAPI app + agent execution |
| `db` | PostgreSQL + pgvector |

---

## 🧠 Agent Workflow (High-Level)

1. User creates a run with a research topic
2. Retriever Agent:
   - checks cache
   - fetches papers from OpenAlex if needed
3. Extractor Agent:
   - extracts structured information per paper
4. Synthesizer Agent:
   - generates literature synthesis
5. Gap Analysis Agent:
   - identifies research gaps & contradictions
6. Hypothesis Agent:
   - proposes testable research hypotheses
7. Artifacts are saved to the database

---