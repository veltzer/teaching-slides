---
tags:
  - observability:tracing
level: intermediate
category: observability
audience:
  - audiences:devops
  - audiences:developers

---

# Using Traces

---

## What This Chapter Covers

- The trace UI
- Searching
- Comparing traces
- Service map
- Debugging workflows

---

## Trace UI

- Tree of spans
- Time on horizontal axis
- Width is duration
- Click for details

---

## Reading A Trace

- Long bars are slow operations
- Gaps mean waiting time
- Many siblings means parallel work
- Find the critical path

---

## Searching

- By service
- By operation
- By tag
- By error

---

## Time Range

- Default last hour
- Wider for rare issues
- Narrow for incident debugging
- Save time ranges in URLs

---

## Comparing Traces

- Side by side
- Fast vs slow
- Find divergence
- Useful for regressions

---

## Service Map

- Auto-built from traces
- Shows call graph
- Latency per edge
- Useful for new joiners

---

## Workflow For Latency Bug

- Filter by slow traces
- Inspect critical path
- Drill into the slowest span
- Read its logs

---

## Diagnose Workflow

![diagnose_workflow](svg/courses/observability_and_monitoring/jaeger/03_using_traces/diagnose_workflow.svg)

---

## Workflow For Errors

- Filter by error tag
- Look at parent span context
- Read attached log entry
- Cross-reference logs system

---

## Linking To Logs

- Correlate by trace ID
- Click from trace to logs
- Or logs to trace
- Saves context-switching

---

## Three Pillars

![trace_to_logs](svg/courses/observability_and_monitoring/jaeger/03_using_traces/trace_to_logs.svg)

---

## Linking To Metrics

- Tag-based panels
- Drill into metric anomaly via traces
- Surface flame graphs from spans
- Connected workflow

---

## Sampling Surprises

- Some related calls missing
- Trace looks broken
- Tail-based fixes most cases
- Verify sampler config

---

## Retention

- Bounded by storage
- Days or weeks typical
- Long retention for compliance
- Tune to budget

---

## Permissions

- Restrict who sees traces
- Sensitive data may live in spans
- Audit access
- Train teams

---

## Common Trace Use Mistakes

- Searching across years
- One trace per investigation
- Ignoring service map
- No link to logs
- Treating sampler artifacts as bugs
