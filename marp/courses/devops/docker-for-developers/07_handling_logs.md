# Handling Logs

---

## Docker Logging Overview

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd0_06_handling_logs" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="50" width="140" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="72" text-anchor="middle" font-size="11" font-weight="bold">Application</text>
  <text x="90" y="90" text-anchor="middle" font-size="10">writes to</text>
  <text x="90" y="105" text-anchor="middle" font-size="10" fill="#555">stdout / stderr</text>
  <line x1="160" y1="85" x2="218" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_06_handling_logs)"/>
  <rect x="220" y="40" width="160" height="90" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="62" text-anchor="middle" font-size="11" font-weight="bold">Docker Daemon</text>
  <text x="300" y="80" text-anchor="middle" font-size="10">Captures streams</text>
  <text x="300" y="95" text-anchor="middle" font-size="10">Applies log driver</text>
  <text x="300" y="110" text-anchor="middle" font-size="10" fill="#555">(json-file default)</text>
  <line x1="380" y1="85" x2="438" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_06_handling_logs)"/>
  <rect x="440" y="50" width="140" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="72" text-anchor="middle" font-size="11" font-weight="bold">Log Storage</text>
  <text x="510" y="90" text-anchor="middle" font-size="10">/var/lib/docker/</text>
  <text x="510" y="105" text-anchor="middle" font-size="10" fill="#555">containers/&lt;id&gt;/</text>
  <rect x="20" y="155" width="560" height="30" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#555">docker logs &lt;container&gt; reads from the configured log driver</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_06_handling_logs" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="130" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="40" text-anchor="middle" font-size="11" font-weight="bold">daemon.json</text>
  <text x="85" y="57" text-anchor="middle" font-size="10" fill="#555">Global config</text>
  <line x1="150" y1="45" x2="218" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_06_handling_logs)"/>
  <text x="185" y="37" text-anchor="middle" font-size="10" fill="#666">sets default</text>
  <rect x="220" y="15" width="160" height="65" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="35" text-anchor="middle" font-size="11" font-weight="bold">Log Driver</text>
  <text x="300" y="52" text-anchor="middle" font-size="10">json-file | syslog</text>
  <text x="300" y="67" text-anchor="middle" font-size="10">journald | splunk</text>
  <line x1="380" y1="45" x2="438" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_06_handling_logs)"/>
  <text x="410" y="37" text-anchor="middle" font-size="10" fill="#666">output</text>
  <rect x="440" y="20" width="140" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="40" text-anchor="middle" font-size="11" font-weight="bold">Log Destination</text>
  <text x="510" y="57" text-anchor="middle" font-size="10" fill="#555">File / Remote / Service</text>
  <rect x="20" y="100" width="560" height="80" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="120" text-anchor="middle" font-size="10" fill="#555">Per-container override: docker run --log-driver=syslog myapp</text>
  <text x="300" y="140" text-anchor="middle" font-size="10" fill="#555">Global default: /etc/docker/daemon.json {"log-driver": "json-file"}</text>
  <text x="300" y="160" text-anchor="middle" font-size="10" fill="#555">Log options: --log-opt max-size=10m --log-opt max-file=3</text>
</svg>

---

## Writing Application Logs

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="30" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="98" text-anchor="middle" font-size="12" fill="white" font-weight="bold">App Logs</text>
  <text x="300" y="113" text-anchor="middle" font-size="10" fill="white">Best Practice</text>
  <ellipse cx="100" cy="45" rx="75" ry="28" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="100" y="42" text-anchor="middle" font-size="11">stdout</text>
  <text x="100" y="57" text-anchor="middle" font-size="10" fill="#555">Normal output</text>
  <ellipse cx="500" cy="45" rx="75" ry="28" fill="#ffebee" stroke="#333" stroke-width="2"/>
  <text x="500" y="42" text-anchor="middle" font-size="11">stderr</text>
  <text x="500" y="57" text-anchor="middle" font-size="10" fill="#555">Error output</text>
  <ellipse cx="100" cy="165" rx="75" ry="28" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="162" text-anchor="middle" font-size="11">JSON format</text>
  <text x="100" y="177" text-anchor="middle" font-size="10" fill="#555">Structured logging</text>
  <ellipse cx="500" cy="165" rx="75" ry="28" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="500" y="162" text-anchor="middle" font-size="11">No file logging</text>
  <text x="500" y="177" text-anchor="middle" font-size="10" fill="#555">Use stdout only</text>
  <line x1="245" y1="78" x2="165" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="78" x2="435" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="245" y1="122" x2="165" y2="148" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="122" x2="435" y2="148" stroke="#333" stroke-width="1.5"/>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd3_06_handling_logs" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="15" width="80" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="38" text-anchor="middle" font-size="10" font-weight="bold">Container</text>
  <text x="60" y="53" text-anchor="middle" font-size="10">A</text>
  <rect x="20" y="80" width="80" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="103" text-anchor="middle" font-size="10" font-weight="bold">Container</text>
  <text x="60" y="118" text-anchor="middle" font-size="10">B</text>
  <rect x="20" y="145" width="80" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="168" text-anchor="middle" font-size="10" font-weight="bold">Container</text>
  <text x="60" y="183" text-anchor="middle" font-size="10">C</text>
  <line x1="100" y1="42" x2="188" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd3_06_handling_logs)"/>
  <line x1="100" y1="107" x2="188" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd3_06_handling_logs)"/>
  <line x1="100" y1="172" x2="188" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd3_06_handling_logs)"/>
  <rect x="190" y="60" width="140" height="80" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="260" y="85" text-anchor="middle" font-size="11" font-weight="bold">Log Collector</text>
  <text x="260" y="102" text-anchor="middle" font-size="10">Fluentd / Logstash</text>
  <text x="260" y="117" text-anchor="middle" font-size="10" fill="#555">Filebeat</text>
  <line x1="330" y1="100" x2="388" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_06_handling_logs)"/>
  <rect x="390" y="60" width="190" height="80" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="485" y="85" text-anchor="middle" font-size="11" font-weight="bold">Central Platform</text>
  <text x="485" y="102" text-anchor="middle" font-size="10">Elasticsearch / Splunk</text>
  <text x="485" y="117" text-anchor="middle" font-size="10" fill="#555">CloudWatch / Grafana Loki</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd4_06_handling_logs" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="11" fill="#555">Log rotation prevents disk exhaustion</text>
  <rect x="30" y="30" width="160" height="75" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="52" text-anchor="middle" font-size="11" font-weight="bold">Active Log</text>
  <text x="110" y="70" text-anchor="middle" font-size="10">container-json.log</text>
  <text x="110" y="87" text-anchor="middle" font-size="10" fill="#555">max-size: 10m</text>
  <line x1="190" y1="67" x2="228" y2="67" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_06_handling_logs)"/>
  <text x="210" y="58" text-anchor="middle" font-size="10" fill="#666">rotate</text>
  <rect x="230" y="30" width="160" height="75" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="310" y="52" text-anchor="middle" font-size="11" font-weight="bold">Rotated Logs</text>
  <text x="310" y="70" text-anchor="middle" font-size="10">log.1, log.2, log.3</text>
  <text x="310" y="87" text-anchor="middle" font-size="10" fill="#555">max-file: 3</text>
  <line x1="390" y1="67" x2="428" y2="67" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_06_handling_logs)"/>
  <text x="410" y="58" text-anchor="middle" font-size="10" fill="#666">oldest</text>
  <rect x="430" y="30" width="150" height="75" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="52" text-anchor="middle" font-size="11" font-weight="bold">Discarded</text>
  <text x="505" y="70" text-anchor="middle" font-size="10">Oldest file removed</text>
  <text x="505" y="87" text-anchor="middle" font-size="10" fill="#555">when limit reached</text>
  <rect x="30" y="125" width="550" height="55" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="305" y="147" text-anchor="middle" font-size="10" fill="#555">Config: --log-opt max-size=10m --log-opt max-file=3</text>
  <text x="305" y="165" text-anchor="middle" font-size="10" fill="#555">Total max disk: max-size x max-file = 30MB per container</text>
</svg>

---

## Monitoring Log Output

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd5_06_handling_logs" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="30" width="140" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="52" text-anchor="middle" font-size="11" font-weight="bold">docker logs -f</text>
  <text x="90" y="72" text-anchor="middle" font-size="10" fill="#555">Follow / stream</text>
  <line x1="160" y1="60" x2="218" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_06_handling_logs)"/>
  <rect x="220" y="30" width="160" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="48" text-anchor="middle" font-size="11" font-weight="bold">Filter + Search</text>
  <text x="300" y="65" text-anchor="middle" font-size="10">--since, --until</text>
  <text x="300" y="80" text-anchor="middle" font-size="10" fill="#555">--tail N, | grep</text>
  <line x1="380" y1="60" x2="438" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_06_handling_logs)"/>
  <rect x="440" y="30" width="140" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="52" text-anchor="middle" font-size="11" font-weight="bold">Analyze</text>
  <text x="510" y="72" text-anchor="middle" font-size="10" fill="#555">Pattern matching</text>
  <rect x="20" y="115" width="560" height="65" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" fill="#555">docker logs --since 2024-01-01 --until 2024-01-02 myapp</text>
  <text x="300" y="152" text-anchor="middle" font-size="10" fill="#555">docker logs myapp 2>&amp;1 | grep ERROR</text>
  <text x="300" y="169" text-anchor="middle" font-size="10" fill="#555">docker logs -f --tail 0 myapp  (only new logs)</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd6_06_handling_logs" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="30" width="140" height="65" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="52" text-anchor="middle" font-size="11" font-weight="bold">No Logs?</text>
  <text x="90" y="68" text-anchor="middle" font-size="10">Check log driver</text>
  <text x="90" y="82" text-anchor="middle" font-size="10" fill="#555">docker inspect</text>
  <line x1="160" y1="62" x2="218" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_06_handling_logs)"/>
  <rect x="220" y="30" width="160" height="65" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="52" text-anchor="middle" font-size="11" font-weight="bold">Disk Full?</text>
  <text x="300" y="68" text-anchor="middle" font-size="10">Add rotation config</text>
  <text x="300" y="82" text-anchor="middle" font-size="10" fill="#555">max-size + max-file</text>
  <line x1="380" y1="62" x2="438" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_06_handling_logs)"/>
  <rect x="440" y="30" width="140" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="52" text-anchor="middle" font-size="11" font-weight="bold">Verify Fix</text>
  <text x="510" y="68" text-anchor="middle" font-size="10">docker logs --tail 5</text>
  <text x="510" y="82" text-anchor="middle" font-size="10" fill="#555">confirm output</text>
  <rect x="20" y="120" width="560" height="60" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="140" text-anchor="middle" font-size="10" fill="#555">Common issue: non-json-file drivers do not support docker logs command</text>
  <text x="300" y="157" text-anchor="middle" font-size="10" fill="#555">Fix: use dual logging mode or query the remote log service directly</text>
</svg>
