# Handling Logs

---

## Docker Logging Overview

![0](../../../out/mermaid/marp/courses/docker-for-developers/06_handling_logs.md/0.png)

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

![1](../../../out/mermaid/marp/courses/docker-for-developers/06_handling_logs.md/1.png)

---

## Writing Application Logs

![2](../../../out/mermaid/marp/courses/docker-for-developers/06_handling_logs.md/2.png)

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

![3](../../../out/mermaid/marp/courses/docker-for-developers/06_handling_logs.md/3.png)

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

![4](../../../out/mermaid/marp/courses/docker-for-developers/06_handling_logs.md/4.png)

---

## Monitoring Log Output

![5](../../../out/mermaid/marp/courses/docker-for-developers/06_handling_logs.md/5.png)

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

![6](../../../out/mermaid/marp/courses/docker-for-developers/06_handling_logs.md/6.png)
