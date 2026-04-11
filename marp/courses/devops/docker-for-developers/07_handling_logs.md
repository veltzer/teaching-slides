---
tags:
  - tools:docker
  - infrastructure:containers
  - practices:devops
  - networking:networking
level: intermediate
category: devops
audience:
  - audiences:developers

---
# Handling Logs

---

## Docker Logging Overview

![docker_logging_overview](svg/courses/devops/docker-for-developers/07_handling_logs/docker_logging_overview.svg)

---

## Log Handlers in Docker

| Handler | Description | Use Case |
|---------|-------------|----------|
| json-file | Default JSON logging | Local development |
| syslog | System logging | System integration |
| journald | systemd journal | Linux systems |
| splunk | Splunk logging | Enterprise monitoring |
| awslogs | AWS CloudWatch | Cloud deployment |

---

## Configuring Log Drivers

![configuring_log_drivers](svg/courses/devops/docker-for-developers/07_handling_logs/configuring_log_drivers.svg)

---

## Writing Application Logs

![writing_application_logs](svg/courses/devops/docker-for-developers/07_handling_logs/writing_application_logs.svg)

---

## Log Driver Configuration

| Option | Purpose | Example |
|--------|---------|---------|
| max-size | Rotate by size | `--log-opt max-size=10m` |
| max-file | Number of files | `--log-opt max-file=3` |
| compress | Compress old logs | `--log-opt compress=true` |
| tag | Custom log tags | `--log-opt tag="{{.Name}}"` |

---

## Structured Logging

```json
{
  "timestamp": "2024-03-15T10:30:00Z",
  "level": "INFO",
  "service": "user-api",
  "message": "Request processed",
  "requestId": "abc-123",
  "duration": 45
}
```

---

## Log Aggregation

![log_aggregation](svg/courses/devops/docker-for-developers/07_handling_logs/log_aggregation.svg)

---

## Common Logging Patterns

| Pattern | Purpose | Example |
|---------|---------|---------|
| Request ID | Track requests | `req-123-abc` |
| Correlation ID | Link related events | `corr-456-xyz` |
| Stack Traces | Debug errors | Include full trace |
| Context | Add metadata | Include user/service info |

---

## Log Rotation Strategy

![log_rotation_strategy](svg/courses/devops/docker-for-developers/07_handling_logs/log_rotation_strategy.svg)

---

## Monitoring Log Output

![monitoring_log_output](svg/courses/devops/docker-for-developers/07_handling_logs/monitoring_log_output.svg)

---

## Log Level Guidelines

| Level | Usage | Example |
|-------|--------|---------|
| ERROR | System failures | Database connection lost |
| WARN | Potential issues | High resource usage |
| INFO | Normal operations | Request completed |
| DEBUG | Troubleshooting | Detailed process info |

---

## Application Logging Code

```python
import logging
import json

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
logger.info(json.dumps({
    'event': 'user_login',
    'user_id': 123,
    'status': 'success'
}))
```

---

## Troubleshooting Logs

![troubleshooting_logs](svg/courses/devops/docker-for-developers/07_handling_logs/troubleshooting_logs.svg)
