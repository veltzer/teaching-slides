---
tags:
  - testing:contract
level: intermediate
category: testing
audience:
  - audiences:developers
  - audiences:testers

---
# Brokers and Workflows

---
## What This Chapter Covers

- Why a broker
- Tags and branches
- Can-I-deploy
- Pending contracts
- Webhooks

---
## What A Broker Is

- Central store for contracts
- Holds verification results
- Computes compatibility
- Powers safe deploy

---
## Why Use One

- Multiple consumers and providers
- Asynchronous teams
- Branch-aware contracts
- Audit trail

---
## Publishing Contracts

- Consumer publishes after generation
- Tag with branch and version
- Broker stores and notifies
- Provider can pull and verify

---
## Tags

- Branch tags
- Environment tags
- Version tags
- Drive compatibility queries

---
## Pending Contracts

- New interaction not yet verified
- Provider can ignore until then
- Avoids breaking provider builds
- Promotes when verified

---
## Can-I-Deploy

- Query broker before deploy
- "Is this consumer compatible with prod provider?"
- Pass or fail
- Wired into deploy pipeline

---
## Compatibility Gate

![can_i_deploy](svg/courses/testing/contract-testing/04_brokers_and_workflows/can_i_deploy.svg)

---
## Webhooks

- Notify provider on new contract
- Trigger verification job
- Notify consumer on verification result
- Closes the loop

---
## Workflow End To End

- Consumer writes test
- Generates contract
- Publishes to broker
- Provider verifies
- Both deploy when compatible

---
## Branch Strategies

- Verify on feature branches
- Promote on main
- Tag environments separately
- Plan with deploy strategy

---
## Multi-Consumer Provider

- One provider, many consumers
- Run all verifications
- Show compatibility matrix
- Useful overview

---
## Deprecation

- Mark old contracts
- Notify consumers
- Set sunset date
- Remove after migration

---
## Audit And Reporting

- Who changed what
- Who verified what
- Compatibility history
- Useful for compliance

---
## Hosted Vs Self-Hosted

- Hosted brokers reduce ops
- Self-hosted gives control
- Pick by scale and policy
- Both common

---
## Common Workflow Mistakes

- No broker, manual sync
- No can-i-deploy gate
- All contracts on one branch
- Webhooks misconfigured
- Stale contracts never cleaned
