---
tags:
  - languages:python
level: advanced
category: language
audience:
  - audiences:developers

---
# Logging in Python

## Overview
- Introduction to Python's logging module
- Logging levels and hierarchy
- Configuration options and methods
- Formatting and handling logs
- Advanced logging techniques
- Best practices for large systems

---
## Why Use Logging?: Limitations of Print Statements

- Hard to control verbosity
- All or nothing output
- Cannot easily route to different destinations
- Difficult to format consistently
- No built-in timestamps or source tracking
- Unsuitable for production environments

```python
# Using print statements - problematic for real applications
def process_data(data):
    print("Starting data processing")

    if not data:
        print("ERROR: Empty data received")
        return None

    print(f"Processing {len(data)} items")
    # Process data...

    if success:
        print("Data processing completed successfully")
    else:
        print("WARNING: Data processing had issues")

    return result
```

---
## Why Use Logging?: Benefits of Proper Logging

- Different severity levels
- Configurable verbosity
- Multiple output destinations
- Consistent formatting
- Timestamp and source information
- Thread safety for concurrent applications
- Hierarchical loggers for component-specific control

```python
# Using proper logging
import logging

logger = logging.getLogger(__name__)

def process_data(data):
    logger.info("Starting data processing")

    if not data:
        logger.error("Empty data received")
        return None

    logger.debug(f"Processing {len(data)} items")
    # Process data...

    if success:
        logger.info("Data processing completed successfully")
    else:
        logger.warning("Data processing had issues")

    return result
```

---
## The Python logging Module: Basic Logging

- Standard library module
- Available in all Python installations
- Multi-level logging system
- Configurable output
- Thread-safe logging
- Hierarchical organization

```python
import logging

# Basic configuration
logging.basicConfig(level=logging.INFO)

# Simple logging messages
logging.debug("This is a debug message")  # Won't show at INFO level
logging.info("This is an info message")    # Will show
logging.warning("This is a warning message")  # Will show
logging.error("This is an error message")  # Will show
logging.critical("This is a critical message")  # Will show

# Output:
# INFO:root:This is an info message
# WARNING:root:This is a warning message
# ERROR:root:This is an error message
# CRITICAL:root:This is a critical message
```

---
## The Python logging Module: Logging Levels

- **DEBUG (10)** - Detailed information, typically for diagnostics
- **INFO (20)** - Confirmation that things are working as expected
- **WARNING (30)** - Something unexpected happened, but the program still works
- **ERROR (40)** - Due to a more serious problem, the program couldn't perform a function
- **CRITICAL (50)** - A serious error indicating the program may be unable to continue running

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set minimum level for this logger

# Example log messages
logger.debug("Detailed information for debugging")
logger.info("Confirmation that things are working")
logger.warning("Something unexpected happened")
logger.error("The program couldn't perform a function")
logger.critical("Serious error, program may not continue")

# You can also specify the level by number
logger.log(logging.INFO, "Another info message")
```

---
## The Python logging Module: Creating Loggers

- `getLogger(name)` creates or retrieves a logger
- Typically use `__name__` as logger name
- Hierarchical organization based on dot notation
- Each component can have its own logger
- Configuration can be inherited and overridden

```python
import logging

# Create loggers
root_logger = logging.getLogger()  # The root logger
app_logger = logging.getLogger("myapp")  # Application logger
db_logger = logging.getLogger("myapp.database")  # Database component
api_logger = logging.getLogger("myapp.api")  # API component

# Module logger (usually best practice)
logger = logging.getLogger(__name__)  # Name based on module

# Hierarchical relationship
print(root_logger.name)  # 'root'
print(app_logger.name)   # 'myapp'
print(db_logger.name)    # 'myapp.database'
print(db_logger.parent.name)  # 'myapp'
```

---
## The Python logging Module: Logger Hierarchy

- Loggers form a tree structure
- Child loggers inherit settings from parents
- Messages propagate up the hierarchy
- Allows for component-specific settings
- Root logger is at the top of the hierarchy

```tree
Logging Hierarchy Example:

root
├── myapp
│   ├── myapp.models
│   │   └── myapp.models.user
│   ├── myapp.views
│   └── myapp.controllers
├── thirdparty
│   └── thirdparty.component
└── other_library
```

```python
# Configuration propagates down, messages propagate up
app_logger = logging.getLogger("myapp")
app_logger.setLevel(logging.INFO)  # All child loggers inherit INFO level
```

---
## Configuring Logging: Basic Configuration

- `basicConfig()` sets up root logger
- Simple way to start logging
- Limited to a single handler
- Fine for simple scripts or applications
- Not sufficient for larger applications

```python
import logging

# Setup basic configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='app.log',
    filemode='w'  # 'w' to overwrite, 'a' to append
)

# Now logs will go to app.log with the specified format
logging.info("Application starting")

# Add console output while keeping file logging
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s: %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
```

---
## Configuring Logging: Using Handlers

- Handlers send log records to destinations
- Multiple handlers can be attached to a logger
- Each handler can have its own level and formatter
- Common handlers:
    - StreamHandler (console)
    - FileHandler (log files)
    - RotatingFileHandler (size-based rotation)
    - TimedRotatingFileHandler (time-based rotation)

```python
import logging
import sys

# Create logger
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

# Create console handler for high-priority messages
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)  # Only WARNING and above

# Create file handler for all messages
file_handler = logging.FileHandler("all.log")
file_handler.setLevel(logging.DEBUG)  # All messages

# Create error file for errors only
error_handler = logging.FileHandler("errors.log")
error_handler.setLevel(logging.ERROR)  # Only ERROR and CRITICAL

# Add all handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(error_handler)
```

---
## Configuring Logging: Using Formatters

- Formatters control log message appearance
- Define timestamp, level, logger name format
- Consistent formatting across handlers
- Custom formats for different outputs
- Special attributes available for formatting

```python
import logging

# Create formatters
simple_formatter = logging.Formatter('%(levelname)s - %(message)s')

detailed_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

json_formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", '
    '"name": "%(name)s", "message": "%(message)s"}'
)

# Create and configure handlers
console_handler = logging.StreamHandler()
console_handler.setFormatter(simple_formatter)

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(detailed_formatter)

json_handler = logging.FileHandler("app.json")
json_handler.setFormatter(json_formatter)
```

---
## Configuring Logging: Format Specification Attributes

- `%(asctime)s` - Human-readable time
- `%(created)f` - Time when record was created (Unix timestamp)
- `%(filename)s` - Filename from which logging was invoked
- `%(funcName)s` - Function name
- `%(levelname)s` - Text logging level ('DEBUG', 'INFO', etc.)
- `%(levelno)d` - Numeric logging level (10, 20, etc.)
- `%(lineno)d` - Line number where logging was invoked
- `%(message)s` - Logged message
- `%(module)s` - Module name
- `%(name)s` - Logger name
- `%(pathname)s` - Full pathname of source file
- `%(process)d` - Process ID
- `%(threadName)s` - Thread name
- `%(thread)d` - Thread ID

---
## Configuring Logging: Dictionary Configuration

- Configure entire logging system at once
- Declarative rather than imperative
- Can be loaded from JSON or YAML files
- More maintainable for complex setups
- Component-based configuration

---

## Dictionary Configuration: Config Dictionary

```python
import logging
import logging.config

# Dictionary-based configuration
config = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'level': 'DEBUG',
            'formatter': 'standard',
        }
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'myapp': {
            'level': 'INFO',
            'propagate': True,  # Send to parent loggers
        }
    }
}
```

---

## Dictionary Configuration: Applying It

```python
# Apply configuration
logging.config.dictConfig(config)

# Use the configured loggers
logger = logging.getLogger("myapp")
logger.info("Application configured with dictConfig")
```

---
## Configuring Logging: File-Based Configuration

- Store configuration in external files
- Multiple configurations for different environments
- Easy to update without code changes
- Common formats: INI, JSON, YAML
- Load with appropriate configuration function

```python
import logging
import logging.config

# Load configuration from file
logging.config.fileConfig('logging.ini')  # INI format

# Or use JSON/YAML format
import yaml
with open('logging.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

# INI file example (logging.ini):
# [loggers]
# keys=root,myapp
#
# [handlers]
# keys=consoleHandler,fileHandler
#
# [formatters]
# keys=simpleFormatter
#
# [logger_root]
# level=DEBUG
# handlers=consoleHandler,fileHandler
#
# [logger_myapp]
# level=INFO
# handlers=
# qualname=myapp
# propagate=1
# ...
```

---
## Configuring Logging: Example YAML Configuration File

```yaml
version: 1
formatters:
  simple:
    format: '%(levelname)s - %(message)s'
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    datefmt: '%Y-%m-%d %H:%M:%S'
handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: simple
    stream: ext://sys.stdout
  file:
    class: logging.FileHandler
    level: DEBUG
    formatter: detailed
    filename: app.log
  errors:
    class: logging.FileHandler
    level: ERROR
    formatter: detailed
    filename: errors.log
loggers:
  myapp:
    level: DEBUG
    handlers: [console, file]
    propagate: no
  myapp.api:
    level: INFO
    handlers: [file]
    propagate: yes
root:
  level: WARNING
  handlers: [console, errors]
```

---
## Using Logging Correctly: Best Practices

- Use module-level loggers with `__name__`
- Use appropriate log levels consistently
- Include contextual information
- Consider log message audience
- Be concise but informative
- Log exceptions with traceback information
- Follow a consistent message format

```python
import logging

# Create module-level logger
logger = logging.getLogger(__name__)

def process_order(order_id, items):
    logger.info("Processing order %s with %d items", order_id, len(items))

    try:
        # Validate order
        if not validate_order(items):
            logger.warning("Order %s failed validation", order_id)
            return False

        # Process payment
        if not process_payment(order_id):
            logger.error("Payment failed for order %s", order_id)
            return False
```

---

## Best Practices: Shipping and Error Handling

```python
        # Ship order
        tracking = ship_order(order_id, items)
        if tracking:
            logger.info("Order %s shipped, tracking: %s", order_id, tracking)
            return True
        else:
            logger.error("Shipping failed for order %s", order_id)
            return False

    except Exception as e:
        logger.exception("Unexpected error processing order %s", order_id)
        # The exception method logs the full traceback
        return False
```

---
## Using Logging Correctly: Log Level Guidelines

- **DEBUG** - Detailed diagnostic information
    - Variable values, function call parameters, SQL queries
    - Internal state changes, loop iterations
    - Only enabled during development/debugging
- **INFO** - Confirmation of normal operation
    - Application startup/shutdown
    - Configuration loaded
    - Tasks started/completed successfully
    - User actions (login, logout, etc.)
- **WARNING** - Non-critical issues, but needs attention
    - Deprecated feature used
    - Resource usage nearing limits
    - Missing optional configuration
    - Automatic recovery from errors
- **ERROR** - Serious problems, function failed
    - Failed to connect to database
    - API request failed
    - Cannot process user input
    - Unhandled exceptions in important operations
- **CRITICAL** - System-wide failures
    - Application cannot start
    - Essential services unavailable
    - Data corruption detected
    - Unrecoverable errors requiring immediate attention

---
## Using Logging Correctly: What to Log

- Application lifecycle events (start, stop)
- Authentication events (login, logout, failures)
- Input validation failures
- Data processing steps
- External service interactions
- Performance metrics
- Security events
- Error conditions and exceptions
- Configuration changes

```python
# Application lifecycle logging
logger.info("Application starting, version %s", __version__)
logger.info("Loading configuration from %s", config_path)
logger.debug("Loaded configuration: %s", config_dict)
logger.info("Initializing database connection")
logger.info("Application ready to serve requests")

# Later...
logger.info("Shutting down application")
logger.info("Closing database connections")
logger.info("Application shutdown complete")
```

---
## Using Logging Correctly: What NOT to Log

- Passwords and access tokens
- Personal identifiable information (PII)
- Credit card numbers
- Health information
- Authentication credentials
- Encryption keys
- Session IDs
- Database connection strings with credentials

```python
# BAD - Logging sensitive information
logger.debug(f"User {username} logged in with password {password}")
logger.info(f"Connected to database with connection string {conn_string}")
logger.debug(f"Credit card info: {cc_number}, {cvv}, {expiration}")

# GOOD - Logging without sensitive information
logger.info(f"User {username} authentication attempt")
logger.info(f"Connected to database {db_name} at {db_host}")
logger.debug(f"Processing payment for order {order_id}")
```

---
## Using Logging Correctly: Using LoggerAdapter for Context

- Add context without modifying log messages
- Pass extra data to all log calls
- Particularly useful for request IDs, user IDs
- Clean way to add context to existing loggers

```python
import logging
from logging import LoggerAdapter

# Create base logger
logger = logging.getLogger(__name__)

# Create adapter with extra context
class RequestAdapter(LoggerAdapter):
    def process(self, msg, kwargs):
        # Add request_id to all messages
        return f'[Request {self.extra["request_id"]}] {msg}', kwargs

# Create adapter instances for different requests
def handle_request(request):
    # Create adapter with request-specific info
    request_logger = RequestAdapter(logger, {"request_id": request.id})

    request_logger.info("Request received")
    # Process request...
    request_logger.debug("Request parameters: %s", request.params)
    # More processing...
    request_logger.info("Request completed")

    # All log messages now include the request_id automatically
```

---
## Using Logging Correctly: Logging Exceptions

- Use `logger.exception()` for exceptions
- Always includes traceback
- Level is automatically ERROR
- Can also use `logger.error()` with `exc_info=True`
- Include relevant context for debugging

```python
import logging

logger = logging.getLogger(__name__)

def risky_operation():
    try:
        # Code that might raise an exception
        result = perform_calculation(data)
        return result
    except ValueError as e:
        # For expected exceptions with specific handling
        logger.error("Invalid data format: %s", str(e))
        return None
    except Exception as e:
        # For unexpected exceptions with full traceback
        logger.exception("Unexpected error in calculation")
        # OR: logger.error("Unexpected error", exc_info=True)
        raise  # Re-raise the exception after logging

# Example output:
# ERROR:module:Unexpected error in calculation
# Traceback (most recent call last):
#   File "module.py", line 8, in risky_operation
#     result = perform_calculation(data)
#   ...
#   ZeroDivisionError: division by zero
```

---
## Using Logging Correctly: Logging in Large Systems

- Use hierarchical logger structure
- Align with package/module structure
- Consistent level usage across components
- Centralized configuration
- Common formatting
- Consider log volume and performance
- Plan for log collection and analysis

```tree
Example Logger Hierarchy for Large System:

myapp                        # Application-wide settings
├── myapp.api                # API component
│   ├── myapp.api.auth      # Authentication API
│   └── myapp.api.endpoints # API endpoints
├── myapp.db                 # Database access
│   ├── myapp.db.models     # Data models
│   └── myapp.db.queries    # DB queries
├── myapp.services          # Business logic services
└── myapp.utils             # Utility functions
```

```python
# Each module creates its own logger
logger = logging.getLogger(__name__)  # e.g., 'myapp.api.auth'

# Configuration can target specific components
logging.getLogger('myapp.db').setLevel(logging.WARNING)  # Less verbose
logging.getLogger('myapp.api').setLevel(logging.DEBUG)   # More verbose
```

---
## Advanced Logging Techniques: Custom Log Levels

- Define your own log levels
- Useful for specific application needs
- Integrate with existing log levels
- Add domain-specific severity

```python
import logging

# Define custom log levels
VERBOSE = 15  # Between DEBUG and INFO
TRACE = 5     # More detailed than DEBUG

# Add level names
logging.addLevelName(VERBOSE, "VERBOSE")
logging.addLevelName(TRACE, "TRACE")

# Add methods to Logger class
def verbose(self, message, *args, **kwargs):
    if self.isEnabledFor(VERBOSE):
        self._log(VERBOSE, message, args, **kwargs)

def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE):
        self._log(TRACE, message, args, **kwargs)

# Add methods to Logger class
logging.Logger.verbose = verbose
logging.Logger.trace = trace

# Using custom levels
logger = logging.getLogger(__name__)
logger.setLevel(TRACE)
logger.trace("Super detailed message")
logger.verbose("Somewhat detailed message")
```

---
## Advanced Logging Techniques: Custom Formatters

- Format log messages in specific ways
- Handle complex formatting needs
- Format as JSON for log aggregation
- Include color coding for console output
- Filter sensitive information

```python
import logging
import json
import datetime

class JsonFormatter(logging.Formatter):
    """Format log records as JSON objects"""

    def format(self, record):
        log_data = {
            "timestamp": datetime.datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add exception info if available
        if record.exc_info:
            # Format traceback info
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }

        return json.dumps(log_data)
```

---

## Custom Formatters: Using the JSON Formatter

```python
# Use the custom formatter
json_handler = logging.StreamHandler()
json_handler.setFormatter(JsonFormatter())
logger = logging.getLogger(__name__)
logger.addHandler(json_handler)
```

---
## Advanced Logging Techniques: Colored Console Logging

- Make console logs more readable
- Color-code by log level
- Stand out for warnings and errors
- Useful during development
- ANSI color codes or colorama library

```python
import logging

# ANSI color codes
COLORS = {
    'RESET': '\033[0m',
    'RED': '\033[31m',
    'GREEN': '\033[32m',
    'YELLOW': '\033[33m',
    'BLUE': '\033[34m',
    'MAGENTA': '\033[35m',
    'CYAN': '\033[36m',
    'WHITE': '\033[37m',
}

class ColorFormatter(logging.Formatter):
    """Apply colors to different logging levels"""

    LEVEL_COLORS = {
        'DEBUG': COLORS['BLUE'],
        'INFO': COLORS['GREEN'],
        'WARNING': COLORS['YELLOW'],
        'ERROR': COLORS['RED'],
        'CRITICAL': COLORS['MAGENTA'],
    }

    def format(self, record):
        # Apply color based on level
        levelname = record.levelname
        color = self.LEVEL_COLORS.get(levelname, COLORS['WHITE'])
        record.levelname = f"{color}{levelname}{COLORS['RESET']}"

        # Format with colors
        return super().format(record)
```

---

## Colored Console Logging: Handler Setup

```python
# Create colored console handler
console = logging.StreamHandler()
console.setFormatter(ColorFormatter('%(levelname)s: %(message)s'))
logger = logging.getLogger()
logger.addHandler(console)
```

---
## Advanced Logging Techniques: Custom Handlers

- Send logs to custom destinations
- Implement specific handling logic
- Create handlers for databases, APIs, queues
- Batch processing of log records
- Custom filtering for specific destinations

```python
import logging
import requests

class HttpHandler(logging.Handler):
    """Send logs to a remote HTTP endpoint"""

    def __init__(self, url, api_key=None, batch_size=10):
        super().__init__()
        self.url = url
        self.api_key = api_key
        self.batch_size = batch_size
        self.records = []

    def emit(self, record):
        try:
            # Format the record
            log_entry = self.format(record)

            # Add to batch
            self.records.append(log_entry)

            # Send if batch is full
            if len(self.records) >= self.batch_size:
                self.flush()

        except Exception:
            self.handleError(record)
```

---

## Custom Handlers: Flushing the Batch

```python
    def flush(self):
        if not self.records:
            return

        # Send records to HTTP endpoint
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'

        try:
            requests.post(
                self.url,
                json={'logs': self.records},
                headers=headers
            )
            self.records = []
        except Exception as e:
            # Handle sending errors
            print(f"Error sending logs: {e}")
```

---
## Advanced Logging Techniques: Filters

- Control which log records get processed
- Different from log levels
- Based on content, context, or specific conditions
- Can modify log records in-place
- Attach to loggers or handlers

```python
import logging

class SensitiveDataFilter(logging.Filter):
    """Filter out sensitive data from log messages"""

    def __init__(self, patterns=None):
        super().__init__()
        self.patterns = patterns or [
            'password', 'secret', 'token', 'key',
            'credit', 'card', 'ssn', 'social'
        ]

    def filter(self, record):
        # Check if the message contains sensitive data
        message = record.getMessage().lower()

        # Check for sensitive patterns
        for pattern in self.patterns:
            if pattern in message:
                # Redact the message
                record.msg = "REDACTED (contained sensitive information)"
                record.args = ()
                break

        return True  # Always include the record, but modified
```

---

## Filters: Applying the Sensitive Data Filter

```python
# Apply filter to a logger
logger = logging.getLogger(__name__)
sensitive_filter = SensitiveDataFilter()
logger.addFilter(sensitive_filter)

# Example usage
logger.info("User profile updated")  # Normal log
logger.info("User password changed to 'secret123'")  # Will be redacted
```

---
## Advanced Logging Techniques: Redirecting Logs to syslog

- Send logs to system logging service
- Centralized logging on Unix-like systems
- Standard system integration
- Works with log aggregation tools
- Use SysLogHandler from logging.handlers

```python
import logging
from logging.handlers import SysLogHandler

# Create logger
logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)

# Create syslog handler
# Use appropriate address for your system
# - Unix domain socket: '/dev/log', '/var/run/syslog'
# - UDP: ('localhost', 514)
syslog = SysLogHandler(address='/dev/log', facility=SysLogHandler.LOG_USER)

# Set a formatter for syslog
formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
syslog.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(syslog)

# Example usage
logger.info("Application starting")
logger.error("Database connection failed")

# Checking the logs
# $ tail -f /var/log/syslog
# May 10 15:23:34 hostname myapp: INFO Application starting
# May 10 15:23:34 hostname myapp: ERROR Database connection failed
```

---
## Advanced Logging Techniques: Rotating Log Files

- Prevent log files from growing too large
- Rotate based on size or time
- Keep a limited number of backup files
- Automatic log file management
- Use built-in handlers from logging.handlers

```python
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# Create logger
logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

# Size-based rotation (rotate at 5MB, keep 5 backups)
size_handler = RotatingFileHandler(
    "app.log",
    maxBytes=5*1024*1024,  # 5MB
    backupCount=5
)

# Time-based rotation (rotate at midnight, keep 30 days)
time_handler = TimedRotatingFileHandler(
    "app-daily.log",
    when="midnight",
    interval=1,
    backupCount=30
)

# Add formatters and handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
size_handler.setFormatter(formatter)
time_handler.setFormatter(formatter)

logger.addHandler(size_handler)
logger.addHandler(time_handler)
```

---
## Collecting Logs: Log Aggregation

- Collect logs from multiple sources
- Centralize log storage and analysis
- Scale with application growth
- Search and analyze logs efficiently
- Monitor and alert on log patterns

---
## Collecting Logs

![log_aggregation](svg/courses/languages/python/advanced-python/13_logging/log_aggregation.svg)

---
## Collecting Logs: Popular Log Aggregation Tools

- Elastic Stack (Elasticsearch, Logstash, Kibana)
- Graylog
- Splunk
- Datadog
- New Relic
- Fluentd/Fluent Bit
- CloudWatch Logs (AWS)
- Stackdriver Logging (GCP)
- Azure Monitor

```python
# Example Elastic Stack integration with python-logstash
import logging
from logstash_async.handler import AsynchronousLogstashHandler

# Create logger
logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)

# Create async logstash handler
logstash_handler = AsynchronousLogstashHandler(
    host='logstash.example.com',
    port=5959,
    database_path='logstash.db'
)

# Add handler to logger
logger.addHandler(logstash_handler)

# Now all logs will be sent to Logstash
logger.info("This log will be sent to Logstash")
```

---
## Collecting Logs: Structured Logging

- Add structure to log messages
- Easier to parse and analyze
- Better for log aggregation
- Common formats: JSON, key=value pairs
- Enable advanced searches and filtering

```python
import logging
import json

class StructuredMessage:
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        # Generate key=value format or JSON
        return f"{self.message} " + " ".join(f"{k}={v}" for k, v in self.kwargs.items())

# Helper function for structured logging
def log_structured(logger, level, message, **kwargs):
    # Only log if the level is enabled
    if logger.isEnabledFor(level):
        logger._log(level, StructuredMessage(message, **kwargs), ())

# Example usage
logger = logging.getLogger(__name__)
log_structured(logger, logging.INFO, "User logged in", user_id=12345,
               source_ip="192.168.1.1", auth_method="password")

# Output: INFO:myapp:User logged in user_id=12345 source_ip=192.168.1.1 auth_method=password
```

---
## Collecting Logs: Distributed Tracing

- Track requests across multiple services
- Correlate logs from different components
- Use correlation IDs to link related logs
- Analyze service dependencies and bottlenecks
- OpenTelemetry, Jaeger, Zipkin integration

```python
import logging
import uuid
from contextvars import ContextVar

# Context variable to hold the trace ID
trace_id = ContextVar('trace_id', default=None)

class TraceFilter(logging.Filter):
    """Add trace ID to log records"""

    def filter(self, record):
        current_trace_id = trace_id.get()
        if current_trace_id:
            record.trace_id = current_trace_id
        else:
            record.trace_id = "no-trace"
        return True
```

---

## Distributed Tracing: Decorator and Configuration

```python
# Decorator to set trace for a request
def with_trace(func):
    async def wrapper(*args, **kwargs):
        # Generate or extract trace ID
        request_trace_id = kwargs.get('trace_id', str(uuid.uuid4()))

        # Set the trace ID for this context
        token = trace_id.set(request_trace_id)
        try:
            return await func(*args, **kwargs)
        finally:
            # Reset the trace ID
            trace_id.reset(token)
    return wrapper

# Configure logger with trace filter
logger = logging.getLogger(__name__)
logger.addFilter(TraceFilter())
formatter = logging.Formatter('%(asctime)s - [%(trace_id)s] - %(message)s')
```

---
## Flushing Logs: Ensuring Logs Are Written

- Logs may be buffered
- Critical to flush in exceptional cases
- Ensure logs are written before crash
- Handler's flush() and close() methods
- Logging shutdown procedure

```python
import logging
import atexit
import signal

def flush_all_logs():
    """Flush all log handlers to ensure logs are written."""
    logging.shutdown()

# Register flush on normal exit
atexit.register(flush_all_logs)

# Register signal handlers for abnormal exits
def signal_handler(sig, frame):
    print(f"Caught signal {sig}, flushing logs and exiting")
    flush_all_logs()
    # Exit with non-zero code for abnormal termination
    exit(1)

# Register for common termination signals
signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # kill command

# For critical logs that must be written immediately
def critical_operation():
    try:
        # Something critical
        pass
    except Exception as e:
        logger.critical("Critical error: %s", str(e))
        # Force immediate flush
        for handler in logger.handlers:
            handler.flush()
```

---
## Flushing Logs: Working with File Buffers

- File buffers can delay writing
- Critical for crash recovery
- Balance performance and durability
- Configure buffer size appropriately
- Use flush() for important log messages

```python
import logging

# Create a file handler with no buffering (immediate write)
no_buffer_handler = logging.FileHandler('critical.log', mode='w', buffering=0)

# Create a file handler with line buffering
line_buffer_handler = logging.FileHandler('info.log', mode='w', buffering=1)

# Create a file handler with default buffering (usually fully buffered)
default_handler = logging.FileHandler('debug.log')

# Create loggers with different handlers
critical_logger = logging.getLogger('app.critical')
critical_logger.addHandler(no_buffer_handler)

info_logger = logging.getLogger('app.info')
info_logger.addHandler(line_buffer_handler)

debug_logger = logging.getLogger('app.debug')
debug_logger.addHandler(default_handler)

# Using the loggers
debug_logger.debug("This message may be buffered")
info_logger.info("This message is line buffered, will be written on newline")
critical_logger.critical("This message is written immediately")
```

---
## Flushing Logs: QueueHandler and QueueListener

- Non-blocking logging for performance
- Process logs in separate thread
- Avoid blocking on I/O operations
- Graceful flushing on shutdown
- Part of standard logging.handlers

```python
import logging
import queue
from logging.handlers import QueueHandler, QueueListener

# Create the log queue
log_queue = queue.Queue(-1)  # No limit on size

# Create handlers for the final destination
file_handler = logging.FileHandler("app.log")
console_handler = logging.StreamHandler()

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
```

---

## QueueHandler and QueueListener: Start and Shutdown

```python
# Set up the queue handler
queue_handler = QueueHandler(log_queue)

# Configure logger to use the queue handler
root = logging.getLogger()
root.addHandler(queue_handler)
root.setLevel(logging.INFO)

# Set up the listener
listener = QueueListener(log_queue, file_handler, console_handler)
listener.start()

# Application code logs normally
logging.info("Application starting")
logging.warning("Some warning")

# When shutting down
listener.stop()  # Flushes logs and stops the listener thread
```

---
## Best Practices for Large Systems: Organizing Logging in Large Applications

- Component-based logger hierarchy
- Configuration in central location
- Consistent formatting across components
- Appropriate log levels for different parts
- Balance between detail and performance
- Test logging configuration

```python
# settings.py - Central configuration
import logging.config
import os
import yaml

def setup_logging(
    config_path='logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CONFIG'
):
    """Set up logging configuration."""
    path = os.getenv(env_key, config_path)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

# In your application's main entry point:
# setup_logging()
```

---
## Best Practices for Large Systems: Performance Considerations

- Logging impacts application performance
- Minimize string formatting in hot paths
- Use lazy evaluation for expensive operations
- Consider asynchronous logging for performance-critical code
- Profile logging overhead
- Balance logging detail with performance needs

```python
import logging

logger = logging.getLogger(__name__)

# BAD: Always performs string formatting
def bad_logging(user_data):
    # This formats the string even if DEBUG is disabled
    logger.debug(f"Processing user data: {user_data}")

# GOOD: Conditional formatting
def good_logging(user_data):
    # This only formats if DEBUG is enabled
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Processing user data: %s", user_data)

# BETTER: Lazy evaluation with lambda
def better_logging(user_data):
    # Only evaluates the expensive function if needed
    logger.debug("User statistics: %s",
                lambda: calculate_expensive_stats(user_data))
```

---
## Best Practices for Large Systems: Thread Safety and Concurrency

- Logging module is thread-safe by default
- Be careful with custom formatters and handlers
- Consider QueueHandler for high-concurrency
- Thread-local context for request-specific information
- Watch for contention on log files
- Test logging under load

```python
import logging
import threading
import time
from logging.handlers import QueueHandler, QueueListener
import queue

# Create the shared queue and handlers
log_queue = queue.Queue(-1)
file_handler = logging.FileHandler("app.log")

# Set up the QueueHandler for thread-safe logging
queue_handler = QueueHandler(log_queue)
root = logging.getLogger()
root.addHandler(queue_handler)
root.setLevel(logging.INFO)

# Set up the listener in the main thread
listener = QueueListener(log_queue, file_handler)
listener.start()
```

---

## Thread Safety and Concurrency: Worker Threads

```python
# Worker threads log normally
def worker(worker_id):
    logger = logging.getLogger(f"worker.{worker_id}")
    logger.info("Worker %d starting", worker_id)
    time.sleep(0.1)
    logger.info("Worker %d finishing", worker_id)

# Start multiple threads
threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

# Shutdown when done
listener.stop()
```

---
## Best Practices for Large Systems: Testing Logging Configuration

- Verify logging behavior in tests
- Check log output for expected content
- Test different logging levels
- Validate handler behavior
- Use temporary handlers for testing
- Test error conditions

```python
import logging
import io
import unittest

class TestLogging(unittest.TestCase):
    def setUp(self):
        # Create logger for testing
        self.logger = logging.getLogger("test_logger")
        self.logger.setLevel(logging.DEBUG)

        # Create a string IO object to capture logs
        self.log_stream = io.StringIO()

        # Create a stream handler that writes to our IO object
        self.handler = logging.StreamHandler(self.log_stream)
        self.handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        self.logger.addHandler(self.handler)

    def tearDown(self):
        # Clean up
        self.logger.removeHandler(self.handler)
        self.handler.close()
```

---

## Testing Logging Configuration: Test Methods

```python
    def test_debug_message(self):
        self.logger.debug("Test debug message")
        log_output = self.log_stream.getvalue()
        self.assertIn("DEBUG: Test debug message", log_output)

    def test_error_with_exception(self):
        try:
            1 / 0
        except ZeroDivisionError:
            self.logger.exception("Division error")

        log_output = self.log_stream.getvalue()
        self.assertIn("ERROR: Division error", log_output)
        self.assertIn("ZeroDivisionError", log_output)
        self.assertIn("Traceback", log_output)
```

---
## Summary

## Key Takeaways
- Use appropriate log levels for different information
- Configure logging with handlers and formatters
- Structure logging hierarchy for components
- Add context to log messages
- Collect and aggregate logs for analysis
- Consider performance impact
- Ensure logs are properly flushed
- Test logging behavior

---
## Resources

## Further Reading
- Python logging module documentation
- "Python Logging Cookbook" in Python docs
- "Logging HOWTO" in Python docs
- PyLogging: Python's Logging Library Extensions
- Books: "Python Logging: Power, Simplicity, and Practicality"
- ELK Stack, Graylog, and other tools' documentation
