 # Payday Fintech
A secure, automated, and observable Kubernetes delivery platform enabling continuous deployment, compliance-ready security gates, and SLO-driven operations for Payday's payments API.


📖 Overview

Problem: Payday's engineering team released weekly but suffered frequent deployment failures, environment drift, slow rollbacks (~45 min), and regulatory friction due to inconsistent audit trails.
Solution: This platform replaces manual processes with a developer-first, security-by-design GitOps pipeline that: ✅ Automates build → test → scan → sign → deploy
✅ Enables safe canary/blue-green releases with automatic SLO-based rollback
✅ Provides full-stack observability (metrics, logs, traces) tied to business SLOs
✅ Enforces least-privilege access, encrypted secrets, and policy-as-code
✅ Reduces rollback time to <2 minutes and change failure rate to <2%

# Architecture;

Developer → GitHub → CI Pipeline → Docker Image → Security Scan → Registry (ECR)
→ GitOps Repo → Argo CD → Kubernetes Cluster
→ Observability Stack (Prometheus + Grafana + Loki + Jaeger)

Graphical representation- LR
    A[Developer Push] --> B[GitHub Actions CI]
    B --> C[Tests + SAST + Trivy Scan + Cosign Sign]
    C --> D[Push to GHCR]
    D --> E[Update GitOps Manifest]
    E --> F[Argo CD Sync]
    F --> G[Argo Rollouts Canary]
    G --> H[Prometheus/Grafana SLOs]
    H --> I{SLO Breach?}
    I -->|Yes| J[Auto-Rollback <2m]
    I -->|No| K[Promote 100% Traffic]
    style A fill:#E0E7FF
    style J fill:#FEE2E2
    style K fill:#D1FAE5

🛠️ Tech Stack


Category                      Tool                    Purpose
Cloud & Cluster           AWS EKS, VPC, KMS  Managed Kubernetes with encrypted control plane & secrets
Infrastructure as Code    Terraform          Declarative provisioning of VPC, EKS, IAM, KMS, S3
CI/CD                     GitHub Actions     Automated testing, scanning, signing, and GitOps updates
GitOps & Deployment       Argo CD,           Declarative sync, canary/blue-green strategies
                          Argo Rollouts
Package Management        Helm               Templated, environment-aware Kubernetes manifests
Observability             Prometheus,        Metrics, logging, tracing, SLO dashboards, alerting
                          Grafanna, Loki, 
                          Jaeger.
Security & Policy         Trivy, Cosign,      CVE scanning, image signing, admission control, KMS-backed secrets
                          QPA/Gatkeeper, 
                          External Secrets.
Backup & DR               Velero              Cluster & stateful workload backup/restore to S3
Autoscaling               HPA, KEDA           CPU/memory & event-driven scaling with cost-aware quotas


# Repository Structures

.
├── infra/terraform/          # AWS VPC + EKS + IAM + KMS provisioning
├── .github/workflows/        # CI/CD pipeline definitions
├── charts/payday/            # Helm chart + Argo Rollouts config
├── argocd/apps/              # GitOps Application & ApplicationSet manifests
├── observability/            # Prometheus, Grafana, Loki, Alertmanager configs
├── runbooks/                 # Incident response, rollback & recovery procedures
├── docs/                     # Architecture diagrams, demo scripts, compliance mapping
└── README.md

# Payday Infrastructure Resources Management by Terraform

Terraform code to provision:
- AWS VPC
- EKS Kubernetes Cluster
- Remote Terraform state (S3)

## Setup

1. Install Terraform & AWS CLI
2. Configure AWS credentials
3. Run:

terraform init
terraform plan
terraform validate
terraform apply

# Kubernetes & Helm Charts

1. 
