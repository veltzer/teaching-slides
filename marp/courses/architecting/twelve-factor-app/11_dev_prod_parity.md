---
tags:
  - concepts:architecture
  - practices:devops
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops

---

# Factor X: Dev/Prod Parity

---

## The Rule

- Keep development, staging, and production as similar as possible
- Differences are accidental complexity that produce production-only bugs
- Closing the gap is a continuous discipline, not a one-time setup

---

## Three Parity Gaps

![parity_gaps](svg/courses/architecting/twelve-factor-app/11_dev_prod_parity/parity_gaps.svg)

---

## Three Gaps to Close

- **Time gap**: code written today reaches production weeks later
- **Personnel gap**: developers write code, ops deploys it
- **Tools gap**: dev uses SQLite, prod uses Postgres; dev uses local file, prod uses S3

---

## Time Gap

- Long delay between commit and prod = forgotten context, drift, hidden incompatibilities
- Continuous deployment shrinks this to hours or minutes
- Even without CD, weekly releases beat quarterly ones
- The shorter the gap, the smaller the surprise

---

## Personnel Gap

- "Dev wrote it; ops runs it" — feedback loop is broken
- DevOps culture: developers carry pagers, see operational reality
- Closes the gap by making the same people responsible for both
- Twelve-factor practices are easier when you'll be paged at 3am if they fail

---

## Tools Gap

- The most insidious gap
- "Locally we use SQLite; production uses Postgres" — a transaction works in one and fails in the other
- "Dev mocks the email service" — broken email goes unnoticed until prod
- Use the same backing services everywhere

---

## Containers Reduce the Gap

- The same image in dev and prod
- The same OS, same dependencies, same runtime
- Local docker-compose can spin up real Postgres, Redis, Kafka
- The compatibility surface is the image, not the environment

---

## Local Development With Real Services

- A dev's laptop runs the production-equivalent stack via docker-compose
- Postgres, Redis, the message broker — all real, all local
- Slower than mocks, but catches bugs that mocks hide
- The cost is laptop resources; the gain is fewer prod-only bugs

---

## When Differences Are Inevitable

- Production: 100 nodes, real users, terabytes of data
- Dev: one laptop, fake users, megabytes
- Scale differences are unavoidable
- Behavior differences are not — and that's where the factor focuses

---

## Anti-Patterns

- "Dev uses SQLite, prod uses Postgres"
- "Tests use a mock email sender; prod uses SendGrid"
- "Dev branches are weeks behind main"
- "Only the senior engineer knows how to deploy"
- "Ops runs custom config that dev doesn't know about"

---

## Staging Should Mirror Production

- Same image, same backing services (smaller scale)
- Same deployment process, same monitoring, same alerts
- "Catches what dev didn't" only works if staging is realistic
- A staging that diverges from prod is just another dev environment

---

## Summary

- Close the time, personnel, and tools gaps
- Containers are the most powerful tool for closing the tools gap
- DevOps culture closes the personnel gap
- Continuous deployment closes the time gap
- Discipline, not a one-time configuration
