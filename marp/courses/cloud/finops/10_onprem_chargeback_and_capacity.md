---
tags:
  - infrastructure:onprem
  - practices:finops
  - practices:cost-optimization
level: intermediate
category: cloud
audience:
  - audiences:devops
  - audiences:architects
  - audiences:managers

---
# On-Prem Chargeback and Capacity Planning

---

## The On-Prem Allocation Problem
- One bill for the whole datacenter
- Many teams share the same hardware
- No automatic per-workload billing
- Hard to answer "what does this app cost?"
- Without allocation, no team feels accountable

---

## Showback for On-Prem
- Report cost per team without billing them
- Builds awareness of consumption
- First step toward chargeback
- Requires resource metering and tagging
- Distribute reports widely and regularly

---

## Chargeback for On-Prem
- Actually charge teams for their consumption
- Drives stronger accountability than showback
- Internal billing requires finance buy-in
- Common in large enterprises with cost centers
- Requires accurate metering and trusted data

---

## Showback vs Chargeback

![showback_vs_chargeback](svg/courses/cloud/finops/10_onprem_chargeback/showback_vs_chargeback.svg)

---

## Building a Unit Cost Model
- Pick a unit: vCPU-hour, GB-month, IOPS-hour
- Sum all costs (hardware, power, facilities, staff)
- Divide by total available capacity
- Multiply by actual consumption per team
- Update unit costs annually as costs change

---

## Unit Cost Calculation Example
- Annual rack cost (full TCO): $120,000
- Servers per rack: 20
- Cores per server: 64
- Total cores per rack: 1,280
- Average utilization: 50%
- Effective utilized cores: 640
- Cost per core-year: $120,000 / 640 = $187.50
- Cost per vCPU-hour: $187.50 / 8760 = $0.0214

---

## Tagging in On-Prem
- VMs and containers can carry metadata tags
- vSphere custom attributes, Kubernetes labels
- Tag for team, project, environment, cost center
- Same principles as cloud tagging
- Less mature tooling, more manual enforcement

---

## Resource Metering Sources
- Hypervisor metrics: vSphere, Hyper-V, KVM
- Kubernetes: kube-state-metrics, Prometheus
- Storage arrays: SNMP, vendor APIs
- Network: NetFlow, sFlow
- Aggregate into a central data warehouse

---

## On-Prem Metering Stack

![onprem_metering_stack](svg/courses/cloud/finops/10_onprem_chargeback/onprem_metering_stack.svg)

---

## Capacity Planning Basics
- Forecast demand before buying hardware
- Lead times: 8-16 weeks for new servers
- Storage growth is usually predictable
- Compute growth follows business growth
- Plan 12-18 months ahead minimum

---

## Capacity Headroom
- Never run at 100% capacity
- Industry rule of thumb: order at 70-80% utilization
- Headroom absorbs spikes and failures
- Too much headroom = wasted CapEx
- Too little = emergency procurement at premium prices

---

## Utilization Tracking
- CPU, memory, storage, network per server
- Aggregate by cluster, rack, datacenter
- Track over time to spot trends
- Identify underutilized hardware for consolidation
- Identify hot spots for redistribution

---

## Query Utilization with Prometheus

```promql
# Average CPU utilization across cluster
avg(
  rate(node_cpu_seconds_total{mode!="idle"}[5m])
) by (cluster)

# Memory utilization per host
1 - (
  node_memory_MemAvailable_bytes /
  node_memory_MemTotal_bytes
)

# Storage usage by pool
sum(node_filesystem_size_bytes
  - node_filesystem_avail_bytes) by (pool)
```

---

## Consolidation Opportunities
- Servers running below 20% utilization
- Multiple under-loaded VMs on separate hosts
- Redundant test/dev environments
- Decommission and reclaim, or virtualize harder
- Hypervisor density: VMs per physical host

---

## Private Cloud Models
- VMware vCloud, OpenStack, Apache CloudStack
- Self-service provisioning for internal users
- Quotas and resource limits per project
- Built-in metering for chargeback
- Closer to cloud experience, retains on-prem control

---

## Kubernetes On-Prem
- Bare-metal or VM-based clusters
- Same cost-allocation challenges as cloud K8s
- Kubecost works on-prem too
- Namespace-based chargeback
- Rightsize requests and limits like cloud

---

## Procurement Cycles
- Annual or bi-annual hardware purchases
- Volume discounts for bulk orders
- Vendor relationships matter (Dell, HPE, Lenovo)
- Lead times affect capacity timing
- Negotiate maintenance and support contracts

---

## Forecasting Demand
- Historical growth + planned business changes
- New product launches, acquisitions, peak seasons
- Engage application teams early
- Build worst-case and best-case scenarios
- Revisit forecasts quarterly

---

## Capacity Planning Cycle

![capacity_planning_cycle](svg/courses/cloud/finops/10_onprem_chargeback/capacity_planning_cycle.svg)

---

## Decommissioning Old Hardware
- Track end-of-support dates per asset
- Migrate workloads off aging hardware
- Wipe and dispose securely
- Account for disposal costs
- Reclaim rack space and power budget

---

## Common On-Prem Allocation Pitfalls
- Allocating fixed costs as if variable
- Charging teams for capacity they didn't request
- Ignoring shared services (network, storage)
- One-size-fits-all unit cost across diverse workloads
- Not updating cost models as hardware ages
