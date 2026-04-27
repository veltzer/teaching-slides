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
# On-Prem Cost Fundamentals

---

## Why On-Prem Still Matters
- Many workloads remain on-prem for regulatory or latency reasons
- Hybrid environments are the norm, not the exception
- On-prem cost discipline is older but often less rigorous
- FinOps principles apply to private infrastructure too
- You cannot optimize what you cannot measure

---

## How On-Prem Costs Differ from Cloud
- Costs are mostly fixed once hardware is bought
- Capacity is purchased years in advance
- Utilization drives unit cost, not consumption
- Bills do not arrive monthly per workload
- Allocation is harder without metering

---

## CapEx vs OpEx
- CapEx: capital expense, depreciated over years
- OpEx: operating expense, hits the books immediately
- On-prem hardware is mostly CapEx
- Cloud is almost entirely OpEx
- Tax and accounting treatment differs significantly

---

## CapEx vs OpEx Comparison

![capex_vs_opex](svg/courses/cloud/finops/09_onprem_cost_fundamentals/capex_vs_opex.svg)

---

## Total Cost of Ownership (TCO)
- TCO = all costs over the asset's useful life
- Hardware purchase + maintenance + power + cooling
- Plus space, networking, staff, and software licenses
- Plus disposal at end of life
- Cloud comparisons are meaningless without full TCO

---

## TCO Components
- Hardware: servers, storage, network gear
- Facilities: datacenter space, racks, cabling
- Power and cooling: ongoing operational cost
- Personnel: ops, maintenance, vendor management
- Software: OS, hypervisors, management tools

---

## Hardware Depreciation
- Servers typically depreciated over 3-5 years
- Storage arrays often 5-7 years
- Network equipment 5-7 years
- Straight-line depreciation is most common
- After full depreciation, equipment may still run but counts as "free"

---

## Depreciation Schedule Example
- Server purchase price: $10,000
- Useful life: 5 years
- Annual depreciation: $2,000 (straight-line)
- Year 1 book value: $8,000
- Year 2 book value: $6,000
- Year 3 book value: $4,000
- Year 4 book value: $2,000
- Year 5 book value: $0 (fully depreciated)

---

## Power Costs
- Measured in kilowatt-hours (kWh)
- Server power draw: 200-800W typical, 1-2kW for GPUs
- Industrial power: $0.05-0.15 per kWh
- A 500W server running 24/7: ~$220-660/year in power alone
- Power costs grow with utilization

---

## Cooling Costs
- Roughly equal to compute power draw
- Power Usage Effectiveness (PUE) measures overhead
- PUE = total facility power / IT equipment power
- Industry average PUE: 1.5-1.6
- Best-in-class hyperscalers: PUE 1.1-1.2

---

## Space and Facilities
- Datacenter rack space: $500-2000/month per rack
- Colocation vs owned vs leased
- Cabling, raised floors, fire suppression
- Physical security and access control
- Insurance and compliance costs

---

## Networking Hardware
- Top-of-rack switches, core switches, routers
- Firewalls and load balancers
- Cabling and patch panels
- Bandwidth costs (ISP contracts)
- Often forgotten in TCO calculations

---

## TCO Breakdown Example

![onprem_tco_breakdown](svg/courses/cloud/finops/09_onprem_cost_fundamentals/onprem_tco_breakdown.svg)

---

## Software Licensing
- OS licenses: Windows Server, RHEL subscriptions
- Hypervisor: VMware, Hyper-V, KVM (free vs paid)
- Database licenses (Oracle, SQL Server)
- Per-core or per-socket licensing models
- Often the largest hidden cost

---

## Personnel Costs
- Hardware ops: rack-and-stack, replacement, maintenance
- Network operations and security teams
- Datacenter facility staff
- Vendor management and procurement
- Spread across many workloads, hard to allocate

---

## Hardware Refresh Cycles
- Servers: typically refreshed every 4-5 years
- Storage: 5-7 years (data migration is painful)
- Network: 7-10 years
- Refresh decisions consider performance, support, efficiency
- Plan refreshes well in advance

---

## When to Refresh: Details
- Vendor support is ending (extended support is expensive)
- Power efficiency of new hardware exceeds old
- Performance limits are blocking growth
- Maintenance costs are climbing
- Hardware failure rates are rising

---

## When to Refresh

![hardware_refresh_decision](svg/courses/cloud/finops/09_onprem_cost_fundamentals/hardware_refresh_decision.svg)

---

## Calculating Cost Per Workload
- Allocate hardware cost based on resources consumed
- Include depreciation, power, cooling, facilities
- Spread shared costs (network, storage) by usage
- Build a unit cost: $/vCPU-hour, $/GB-month
- Compare against cloud equivalents

---

## Common On-Prem Cost Pitfalls
- Sunk-cost thinking ("we already paid for it")
- Ignoring power and cooling in cost models
- Counting only hardware, not staff or facilities
- Over-provisioning for peak loads
- Not tracking utilization across the fleet
