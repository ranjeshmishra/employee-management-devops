
# Employee Management DevOps Project

## Project Overview
A production-style three-tier Employee Management application.

## Technology Stack
- Frontend: Web application
- Backend: Python FastAPI
- Database: PostgreSQL
- Container Runtime: containerd
- Container Image Registry: GitHub Container Registry (GHCR)
- Orchestration: Kubernetes
- CI/CD: GitHub Actions
- GitOps: Argo CD
- Monitoring: Prometheus and Grafana

## Project Structure
- backend/ - FastAPI source code
- frontend/ - Frontend application
- database/ - PostgreSQL database scripts
- k8s/ - Kubernetes manifests
- .github/workflows/ - CI/CD workflows
- docs/ - Documentation
- scripts/ - Automation scripts

## Deployment Environment
- Master: 192.168.1.101
- Worker1: 192.168.1.102
- Worker2: 192.168.1.104
- Kubernetes: v1.30.8
- Container Runtime: containerd 2.2.6

## Project Status
Stage 1 - Environment and Git setup
