# Cost analysis

This document summarizes the current infrastructure cost profile for the Payday EKS deployment and highlights the effect of using `t3a.medium` Spot capacity.

## Current compute assumption

The Terraform EKS node group currently targets:

- `t3a.medium`
- `SPOT`
- `min_size = 2`
- `desired_size = 5`
- `max_size = 6`

## Estimated compute cost

### Spot node estimate

A `t3a.medium` instance is approximately `0.0416 USD/hour` on demand in `us-east-2`.

Spot capacity is variable, but a typical savings range is often **40% to 70%** below on-demand pricing. For planning purposes, a realistic operational estimate is:

- **Lower savings bound:** 40% off on-demand
- **Typical savings target:** 55% off on-demand

### Monthly estimate for 5 nodes

| Scenario | Per-node hourly rate | Nodes | Monthly estimate |
| --- | ---: | ---: | ---: |
| On-demand | $0.0416 | 5 | $152.00 |
| Spot (40% savings) | $0.0250 | 5 | $91.00 |
| Spot (55% savings) | $0.0187 | 5 | $68.00 |

> These numbers are budget estimates and do not include control plane, storage, or data transfer costs.

## Other cost drivers

### EKS control plane

The managed EKS control plane typically adds an ongoing charge. A common planning assumption is roughly **$0.10/hour**, which is about **$73/month**.

### Storage

- Bitnami PostgreSQL persistent volumes add storage cost
- The exact cost depends on volume size and IOPS profile
- Additional snapshots or backups increase storage usage

### Load balancing and networking

- Service and ingress resources add traffic and load balancer costs
- These costs depend on whether you use AWS load balancers or an alternative ingress controller

## Impact of Spot capacity

Using Spot nodes reduces worker-node spend significantly, but it introduces operational risk:

- node termination may occur during capacity auctions
- workload churn increases during cost-driven rebalancing
- the cluster needs fast recovery and alerting

### Practical recommendation

- Use Spot nodes for the worker pool
- Keep the **minimum size** high enough for steady-state workloads
- Add alerting on node evictions and pod restarts
- Maintain a small on-demand fallback if uptime is critical

## Current recommendation

For this repo, the current `t3a.medium` Spot configuration is a strong cost optimization choice for non-critical workloads, especially when combined with:

- Argo Rollouts for safe rollout control
- automated health checks
- Grafana and alerting for operational visibility

## Suggested cost guardrails

1. Track monthly worker-node spend by namespace and environment
2. Review Spot interruption events weekly
3. Compare app availability against compute cost savings
4. Consider a small on-demand fallback if the application has strict availability requirements
5. Add a node-group budget alert for sustained capacity use

## Suggested next steps

- Add a Grafana dashboard for node utilization and Spot interruption rate
- Add alerting for repeated evictions and rollout failures
- Document the storage sizing for PostgreSQL and the expected monthly storage cost
- Review whether a small on-demand pool is required for baseline availability
