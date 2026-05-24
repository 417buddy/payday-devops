# Runbook

This runbook covers day-to-day operations, incident response, rollback, and recovery for the Payday platform.

## Scope

This runbook applies to:

- Backend service `payday-api`
- Frontend service `payday-app`
- EKS cluster managed by Terraform
- Bitnami PostgreSQL
- Prometheus, Grafana, and alerting

## Prerequisites

Before operating the environment, confirm that the following are available:

- AWS CLI configured with access to the target account
- `kubectl` configured for the EKS cluster
- `argocd` CLI installed
- `kubectl-argo-rollouts` installed
- Access to the target namespace `payday`

## Service commands

### Check rollout status

```bash
kubectl argo rollouts get rollout payday-api -n payday
kubectl argo rollouts get rollout payday-app -n payday
```

### Trigger Argo CD sync

```bash
argocd app sync payday-api
argocd app sync payday-app
```

### Roll back a rollout

```bash
kubectl argo rollouts abort payday-api -n payday
kubectl argo rollouts abort payday-app -n payday
```

### Promote a rollout manually

```bash
kubectl argo rollouts promote payday-api -n payday
kubectl argo rollouts promote payday-app -n payday
```

## Deployments

### Backend deployment

1. Confirm the backend workflow is green in GitHub Actions
2. Verify the image exists in GHCR
3. Ensure Argo CD is healthy
4. Allow the workflow to update the Helm values and trigger sync
5. Verify the rollout is healthy

### Frontend deployment

1. Confirm the frontend workflow is green in GitHub Actions
2. Verify the image exists in GHCR
3. Trigger or allow Argo CD sync
4. Verify the rollout health

## Rollback procedures

### Rollback due to a failed canary

Use the Argo Rollouts abort command when a deployment is degraded:

```bash
kubectl argo rollouts abort payday-api -n payday
kubectl argo rollouts abort payday-app -n payday
```

### Rollback due to a bad application release

If the application is healthy in the cluster but behavior is incorrect:

1. Abort the current rollout if it is still progressing
2. Confirm the previous stable revision is restored
3. Verify service health and smoke tests
4. Confirm Argo CD sync is clean

## Incident response

### 1. Confirm the scope

Check the current rollout status and the affected service:

```bash
kubectl argo rollouts get rollout payday-api -n payday
kubectl argo rollouts get rollout payday-app -n payday
kubectl get pods -n payday
```

### 2. Check API and readiness

For the backend, validate the health endpoints:

```bash
curl -sf http://<service>/health
curl -sf http://<service>/ready
```

### 3. Check Prometheus and alerting

Inspect Prometheus alerts and Grafana dashboards for service errors, latency spikes, or resource saturation.

### 4. Check database health

Inspect the PostgreSQL pod and confirm connectivity:

```bash
kubectl get pods -n payday | grep postgres
kubectl logs -n payday deploy/postgres-postgresql
```

## Spot interruption response

The EKS managed node group uses `t3a.medium` Spot capacity. If the node is reclaimed:

1. Confirm the node termination and pod eviction events
2. Check which workloads were affected
3. Ensure the pod scheduler re-creates the workloads on remaining capacity
4. Validate that `payday-api` and `payday-app` recover cleanly
5. Review metrics for restart spikes or request errors

## PostgreSQL recovery

If PostgreSQL becomes unavailable:

1. Validate the PostgreSQL pod and PVC status
2. Confirm the backend is using the expected service name
3. Verify database connectivity from the backend pod
4. If needed, restore the Bitnami PostgreSQL release from backup or recreate the release

## Prometheus and Grafana

### Prometheus

- Confirm `payday-api` is scraping `/metrics`
- Validate service discovery targets
- Ensure alert rules are loaded successfully

### Grafana

- Confirm dashboards are present and bound to the Prometheus datasource
- Review rollout, app health, and database dashboards

### Alerting

Typical alert categories:

- High error rate
- Increased latency
- Pod restart loops
- CPU or memory saturation
- PostgreSQL unavailability
- Spot capacity pressure

## Capacity and scaling

If the cluster is under pressure:

1. Review node utilization
2. Inspect HPA or replica settings in the Helm charts
3. Increase the desired size of the managed node group if necessary
4. Rebalance workload placement if Spot interruptions are causing repeated churn

## Troubleshooting checklist

- Argo CD sync status is healthy
- Argo Rollouts rollout is healthy
- Backend and frontend pods are running
- PostgreSQL pod is running and writable
- Prometheus targets are up
- Grafana dashboards are loading
- Alerting is not muted or suppressed

## Escalation

Escalate to platform or SRE ownership when:

- Argo CD remains unhealthy for more than 10 minutes
- Rollouts fail repeatedly
- PostgreSQL is unavailable or corruption is suspected
- Spot interruption causes sustained service degradation
- Alerting is unavailable during an active incident

## Recommended improvements

- Add explicit PodDisruptionBudgets for Spot resilience
- Add automated alert routing for rollout failures
- Add Grafana dashboards for canary metrics and database health
- Add a documented backup and restore procedure for PostgreSQL
