---
tags:
  - data-and-ai:airflow
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Sensors

---
## Sensor Modes

![sensor_modes](svg/courses/data_engineering/apache-airflow/04_sensors/sensor_modes.svg)

---
## What This Chapter Covers

- What sensors are
- Common sensors
- Modes: poke vs reschedule
- Deferrable operators
- Timeouts

---
## What A Sensor Is

- Wait for a condition
- Then proceed
- "Wait for file in S3"; "Wait for SQL row"
- Poll until condition met

---
## Common Sensors

- S3KeySensor: file in S3
- ExternalTaskSensor: another DAG's task
- HttpSensor: URL responds
- SqlSensor: query returns rows
- TimeDeltaSensor: wait N seconds

---
## S3KeySensor

```python
S3KeySensor(
    task_id='wait_for_data',
    bucket_key='data/2026-05-01/file.csv',
    bucket_name='my-bucket',
    timeout=60 * 60 * 6,  # 6 hours
    poke_interval=300       # 5 min
)
```

---
## Modes: Poke

- Default
- Holds a worker slot while waiting
- Wastes resources
- For: short waits

---
## Modes: Reschedule

```python
S3KeySensor(..., mode='reschedule')
```

- Releases worker between checks
- Schedules next check
- Better for long waits

---
## Deferrable Operators

- Newer alternative
- Defer work to a triggerer process
- No worker slot held
- Best for: production at scale

---
## Timeouts

- Sensor times out: task fails
- Set explicit timeout
- Default: timeout=conf.timeout (week or so)
- Without: sensor can hang forever

---
## ExternalTaskSensor

- Wait for another DAG's task to complete
- Cross-DAG dependencies
- Brittle; consider events instead

---
## Dataset Triggers

- Modern alternative to sensors for cross-DAG
- One DAG produces a Dataset; another consumes
- More robust than ExternalTaskSensor

---
## SQL Sensor

- Wait for query to return rows
- Useful: wait for downstream system to populate
- Poll interval set carefully

---
## When To Use Sensors

- Wait for external file / data
- Wait for system A to publish before system B consumes
- Wait until time-based event

---
## When Not To

- Long-running waits without reschedule mode
- "Wait for nothing in particular" — use a delay instead
- For event-driven, use Datasets

---
## Common Sensor Mistakes

- Default poke mode for hours-long waits (resource hog)
- No timeout (hangs)
- Polling too frequently (wasted reads)
- ExternalTaskSensor across non-aligned DAGs (deadlocks)
- Sensors that should be event listeners

---
## Common Sensor Use Cases

![sensor_use_cases](svg/courses/data_engineering/apache-airflow/04_sensors/sensor_use_cases.svg)
