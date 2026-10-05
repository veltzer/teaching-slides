---
tags:
  - data-and-ai:ai
  - data-and-ai:generative-ai
  - concepts:code-generation
  - tools:github
  - practices:productivity
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:team-leads
  - audiences:devops

---

# Administering Copilot in an Organization

---

## What This Chapter Covers

- Seats: who gets Copilot, and for how long
- Policies: which features, models and previews are allowed
- Data: what leaves the organization and what is retained
- Content exclusion: what it hides and where it leaks
- Audit log events and usage metrics
- Rolling Copilot out: pilots, champions and a decision checklist

---

## Where Administration Happens

- `Copilot Business`: settings live in the organization
- `Copilot Enterprise`: settings start at the enterprise account
- The enterprise can enable, disable or delegate each policy
- Delegated policies are decided by each organization
- Users only see the result; they cannot override a disabled policy
- Settings path: organization **Settings** → **Copilot**

---

## Policy Inheritance

![policy_inheritance](svg/courses/ai/github-copilot-in-practice/09_administering_copilot_in_an_organization/policy_inheritance.svg)

---

## Assigning Seats

- Seats are billed per assigned user per month
- Assign to all members, or to selected teams and users
- Prefer teams: membership changes update seats automatically
- Mirror teams from your identity provider with team sync or `SCIM`
- A seat not used for a while is still billed: review inactive seats
- The `REST` API can add and remove seats in bulk

---

## Seat Management with the API

```bash
# Add a team to Copilot
gh api -X POST /orgs/acme/copilot/billing/selected_teams \
    -f "selected_teams[]=backend"

# List seats with their last activity
gh api /orgs/acme/copilot/billing/seats \
    --jq '.seats[] | [.assignee.login, .last_activity_at] | @tsv'
```

---

## Contractors and Short-Lived Access

- Put contractors in a dedicated team with its own seat assignment
- Removing them from the team removes the seat at the next cycle
- Outside collaborators cannot get a seat from the organization
    - They need their own license or membership
- Decide up front whether contractor code may be sent to Copilot at all
- Automate expiry: an access review that removes the team membership
- Pending cancellation keeps access until the end of the billing cycle

---

## Policy Areas

| Area | Typical choice | Why it matters |
|---|---|---|
| Copilot in the IDE | enabled | the baseline feature |
| Chat on `github.com` | enabled | questions about repositories and PRs |
| Agent mode, coding agent | pilot teams first | runs commands, opens PRs |
| `MCP` servers | allowlist | third-party tools see your code |
| Models | curated list | cost multipliers, data terms |
| Preview features | disabled by default | different terms, can change |

---

## Feature-by-Feature Enablement

- Each surface has its own switch: IDE chat, `CLI`, web chat, code review, coding agent
- The coding agent also needs enabling per repository
- Models are switched on one by one; some carry extra terms
- Preview features are off unless someone opts in
- A missing feature in a user's IDE is usually a policy, not a bug
- Document every choice: users will ask why they cannot see something

---

## Premium Requests and Budgets

- Chat, agents and code review consume premium requests
- Each model has a multiplier: a heavy model costs several requests per call
- Every plan includes a monthly allowance per seat
- Above the allowance: blocked, or paid per request
- Set a budget and spending limit at enterprise or organization level
- Watch the usage report before raising limits for everyone

---

## Public Code Matching

- A filter that hides suggestions matching public code (~150 characters)
- **Block**: matching suggestions are never shown
- **Allow**: matches are shown with code references and licenses
- Background: model output can reproduce licensed open source code
- GitHub's IP indemnity for Business and Enterprise requires the filter set to **Block**
- Choose deliberately with your legal team, not by default

---

## What Leaves Your Organization

- Prompts: the code around the cursor, open tabs, chat text, attached files
- Sent over `TLS` to GitHub's Copilot service and model providers
- Business and Enterprise: your code is not used to train models
- Model providers are contractually barred from training on it
- Third-party `MCP` servers are outside these terms
- Preview features may have different data terms

---

## Data Retention

| Surface | Prompts and suggestions | Notes |
|---|---|---|
| IDE code completions | not retained | discarded after the response |
| IDE chat, `CLI`, web chat | retained about 28 days | for abuse monitoring |
| Coding agent | session logs kept with the PR | visible in the repository |
| User engagement data | retained longer | usage metrics, telemetry |

At time of writing — check docs.github.com for current values.

---

## Content Exclusion

- Hides files from Copilot so they are never used as context
- Configured as path patterns in repository or organization settings
- Enterprise can also set exclusions across all organizations
- Changes take up to 30 minutes to reach IDEs
- Excluded files show a disabled Copilot icon in the editor
- Use it for secrets, keys, customer data and regulated code

---

## Content Exclusion Configuration

```yaml
# Organization level: repository reference, then paths
"*":
  - "**/.env"
  - "**/secrets/**"
acme/payments-service:
  - "/src/crypto/**"
  - "*.pem"
git@github.com:acme/legacy-billing.git:
  - "**"
```

---

## What Exclusion Covers

![exclusion_coverage](svg/courses/ai/github-copilot-in-practice/09_administering_copilot_in_an_organization/exclusion_coverage.svg)

---

## The Honest Limits of Exclusion

- It filters what Copilot reads as context, it does not encrypt anything
- Agent mode, the coding agent and the `CLI` have had gaps in support
- An agent running `cat` in a terminal reads whatever the shell can read
- Symbolic links and copies of a file are not excluded
- Semantic information from the language server may still leak through
- Real protection: keep secrets out of the repository in the first place

---

## Copilot in the Audit Log

- Seat assignments and removals
- Policy and setting changes, with who changed them
- Content exclusion changes
- Coding agent and agent activity attributed to the user who started it
- Search with `action:copilot` in the audit log
- Stream the log to your `SIEM` for alerting

---

## Usage Metrics

- Copilot usage metrics dashboard at enterprise and organization level
- Usage metrics `API`: daily data per IDE, language, model and feature
- Active and engaged users, completions, chat turns, agent use
- Per-user reports for seat reviews
- Combine with your own data: PR throughput, review time, incidents

```bash
gh api /orgs/acme/copilot/metrics \
    --jq '.[] | [.date, .total_active_users, .total_engaged_users] | @tsv'
```

---

## Metrics That Mean Something

| Vanity metric | Better question |
|---|---|
| Acceptance rate | Did accepted code survive review and stay? |
| Lines suggested | Did lead time from issue to merge change? |
| Number of chat turns | Did onboarding time to first PR drop? |
| Seats assigned | How many seats were used in the last 30 days? |
| Agent PRs opened | How many agent PRs were merged without rework? |

---

## Why Acceptance Rate Misleads

- Accepting is cheap; deleting the code later is not counted
- Short suggestions inflate the rate
- Experienced developers often reject more and gain more
- It measures the tool, not the outcome for the team
- Use it only to detect broken setups, not to rank people
- Never turn Copilot metrics into individual performance targets

---

## Rollout Phases

![rollout_phases](svg/courses/ai/github-copilot-in-practice/09_administering_copilot_in_an_organization/rollout_phases.svg)

---

## Pilots and Champions

- Pilot with volunteers from several teams and languages
- Measure a baseline before the pilot starts
- Pick one champion per team: answers questions, collects patterns
- Commit shared `.github/copilot-instructions.md` and prompt files early
- Run short internal trainings on real repositories, not toy demos
- Publish an internal FAQ: policies, data terms, how to get help

---

## Decisions Every Organization Must Make

| Decision | Options |
|---|---|
| Plan | `Business` or `Enterprise` |
| Who gets seats | everyone, teams, on request |
| Public code matching | block (indemnity) or allow with references |
| Agents and coding agent | off, pilot teams, everyone |
| Models and previews | curated list or all |
| Budget for premium requests | hard limit or paid overage |

---

## More Decisions

| Decision | Options |
|---|---|
| Content exclusion | which paths and repositories |
| `MCP` servers | none, allowlist, open |
| Contractors | same policy, restricted, none |
| Metrics | which ones, who sees them, never per-person ranking |
| Review policy | Copilot review as first pass, humans approve |
| Ownership | who maintains instructions and policies |

---

## Key Takeaways

- Assign seats through teams and review inactive seats regularly
- Every feature is a policy: decide it on purpose and write it down
- Keep the public code filter on block if you rely on IP indemnity
- Content exclusion reduces exposure; it is not a security boundary
- Measure outcomes, not acceptance rates
- Roll out in phases with champions and shared instructions
