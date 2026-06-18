---
id: SPEC-10-01
title: Production Infrastructure & Containerization
status: draft
phase: 10
sequence: 1
dependencies: [SPEC-01-03, SPEC-08-03]
---

# Production Infrastructure & Containerization

## Overview
This specification defines the production topology, container optimization, and network security for INIVESTEC. Given the hybrid LLM architecture, the infrastructure must intelligently separate CPU-bound web workers from GPU-bound AI inference workloads to optimize costs and performance.

## Goals
1. Create highly optimized, multi-stage Dockerfiles for the FastAPI backend and Next.js frontend.
2. Architect a split-topology deployment: CPU instances for Web/Taskiq/DB, and a dedicated GPU instance for the Local LLM (Ollama).
3. Enforce strict network isolation to ensure the Local LLM is never exposed to the public internet.

## Requirements

### 10.1 Container Optimization
- **Backend (FastAPI + Taskiq)**: Multi-stage Docker build using `python:3.12-slim`. Install only production dependencies. Use `uvicorn` with multiple workers for the API, and a separate container/service for Taskiq workers.
- **Frontend (Next.js 15)**: Multi-stage build using `node:20-alpine`. Leverage Next.js standalone output (`output: 'standalone'`) to minimize the final image size to < 150MB.
- **Database & Cache**: Use managed services for PostgreSQL (with TimescaleDB & pgvector extensions enabled) and Redis in production to offload maintenance and ensure automated backups.

### 10.2 Split-Topology Architecture
- **Control Plane (CPU)**: Hosts Nginx, Next.js, FastAPI, Taskiq Workers, and Redis. Deployed on a standard PaaS (e.g., Railway, Render, or AWS ECS).
- **AI Plane (GPU)**: Hosts the Ollama service running `llama3:8b-instruct` and `nomic-embed-text`. Deployed on a GPU-enabled VPS (e.g., RunPod, Lambda Labs, or AWS G5).
- **Networking**: The AI Plane must be accessible *only* via a secure, authenticated internal tunnel (e.g., Tailscale, Cloudflare Tunnel, or VPC peering) from the Control Plane.

### 10.3 Nginx Reverse Proxy & Security
- **Routing**: Nginx routes `/api/*` to FastAPI, and `/*` to Next.js.
- **Security**: Nginx must explicitly `deny all` external traffic to port `11434` (Ollama) and port `6379` (Redis).
- **Headers**: Inject strict security headers (`Strict-Transport-Security`, `X-Content-Type-Options`, `Content-Security-Policy`).

## Acceptance Criteria
- [ ] `Dockerfile.backend` and `Dockerfile.frontend` are created, utilizing multi-stage builds and passing Docker linting (e.g., `hadolint`).
- [ ] `docker-compose.prod.yml` successfully orchestrates the local production simulation, verifying Nginx routing and service health checks.
- [ ] Network isolation is verified: an external port scan of the production IP shows ports 80/443 open, but 11434 (Ollama) and 5432 (Postgres) strictly closed/filtered.
- [ ] Next.js standalone build size is verified to be under 200MB.

## Out of Scope
- Kubernetes (K8s) orchestration (Docker Compose / PaaS native scaling is sufficient for MVP/Beta).
- CDN configuration for static assets (handled by PaaS/Vercel defaults).

## Technical Details
- **Tools**: Docker, Nginx, Tailscale/Cloudflare Tunnels.
- **Environment Management**: All production secrets must be injected via the PaaS/VPS environment variable manager, never baked into the Docker image.
