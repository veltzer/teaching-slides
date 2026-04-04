# Marp TargetCloseError Analysis

## Root Cause

Running `rsconstruct build -j 20` launches up to 20 concurrent Marp processes,
each spawning a headless Chromium instance via Puppeteer. This causes resource
exhaustion (memory/CPU), leading to non-deterministic Chromium crashes:

```
TargetCloseError: Protocol error (Target.setDiscoverTargets): Target closed
```

Chrome dies before Puppeteer can establish a CDP connection.

## Fix

Add per-processor `max_jobs` support to rsconstruct so that marp can be limited
to e.g. 4 concurrent jobs while other processors use the full `-j` value.

See: `/home/mark/git/veltzer/rsconstruct/docs/src/per-processor-max-jobs.md`

## Workaround (until feature is implemented)

Use a lower global parallelism: `rsconstruct build -j 4`
