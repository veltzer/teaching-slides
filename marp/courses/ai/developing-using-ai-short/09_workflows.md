# Real-World Project Workflows

---

## End-to-End Development with AI

From concept to production using AI assistance

This chapter covers:
1. Project initialization
1. Feature development
1. Bug fixing workflows
1. Code maintenance
1. Release preparation

---

## The Complete Development Cycle

![the_complete_development_cycle](svg/courses/ai/developing-using-ai-short/09_workflows/the_complete_development_cycle.svg)

---

## Project Initialization: Boilerplate Setup

AI generates project structure:

```bash
# AI prompt: "Create a Node.js microservice boilerplate"

my-service/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   ├── middlewares/
│   │   └── validators/
│   ├── services/
│   ├── models/
│   ├── config/
│   └── utils/
├── tests/
├── docker/
├── .github/workflows/
├── package.json
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

Complete scaffold in seconds!

---

## Structure Generation

AI creates initial files:

```javascript
// AI generates package.json with best practices
{
  "name": "my-service",
  "version": "0.1.0",
  "scripts": {
    "start": "node dist/index.js",
    "dev": "nodemon src/index.ts",
    "build": "tsc",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint src/**/*.ts",
    "format": "prettier --write src/**/*.ts"
  },
  "dependencies": {
    "express": "^4.18.0",
    "winston": "^3.8.0",
    "dotenv": "^16.0.0"
  },
  "devDependencies": {
    "@types/node": "^18.0.0",
    "typescript": "^5.0.0",
    "jest": "^29.0.0",
    "eslint": "^8.0.0",
    "prettier": "^2.8.0"
  }
}
```

---

## Tool Configuration

Setting up development environment:

```yaml
# AI generates docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      - mongo
      - redis

  mongo:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  mongo_data:
```

---

## Feature Development: Requirement Analysis

![feature_development_requirement_analysis](svg/courses/ai/developing-using-ai-short/09_workflows/feature_development_requirement_analysis.svg)

---

## Design Discussion

AI helps design features:

```markdown
You: "I need to add user notifications"

AI: "Let's design a notification system:

1. **Types**: Email, Push, In-app
2. **Architecture**:
   - Queue-based (Redis Bull)
   - Event-driven triggers
   - Template system

3. **Database Schema**:
   - notifications table
   - user_preferences table
   - notification_logs table

4. **API Endpoints**:
   - GET /notifications
   - POST /notifications/mark-read
   - PUT /notifications/preferences

5. **Real-time**: WebSocket for instant delivery

Shall we start with the schema?"
```

---

## Implementation Strategy

Breaking down features:

```python
# AI creates implementation plan
class NotificationFeature:
    """
    Implementation Checklist:

    Phase 1: Core Infrastructure (Day 1)
    □ Database schema
    □ Basic models
    □ Queue setup

    Phase 2: Business Logic (Day 2)
    □ Notification service
    □ Template engine
    □ Delivery methods

    Phase 3: API Layer (Day 3)
    □ REST endpoints
    □ WebSocket events
    □ Authentication

    Phase 4: Testing (Day 4)
    □ Unit tests
    □ Integration tests
    □ E2E tests
    """
```

---

## Testing Approach

Comprehensive testing strategy:

```javascript
// AI generates test suite structure
describe('Notification Feature', () => {
  describe('Unit Tests', () => {
    test('should create notification', () => {});
    test('should validate notification data', () => {});
    test('should handle delivery failure', () => {});
  });

  describe('Integration Tests', () => {
    test('should send email notification', () => {});
    test('should queue bulk notifications', () => {});
    test('should respect user preferences', () => {});
  });

  describe('E2E Tests', () => {
    test('complete notification flow', () => {});
    test('real-time delivery via WebSocket', () => {});
  });
});
```

---

## Bug Fixing Workflows: Issue Reproduction

Systematic bug investigation:

```markdown
## Bug Report Analysis

**Issue**: Users report notifications not arriving

**AI Investigation Steps**:
1. Check error logs for exceptions
2. Verify queue is processing
3. Confirm email service is up
4. Test with specific user account
5. Review recent deployments

**Reproduction Script**:
```javascript
// AI generates reproduction test
const reproducer = async () => {
  const user = await createTestUser();
  const notification = await sendNotification(user);
  const received = await checkDelivery(notification);
  assert(received, 'Notification not delivered');
};
```

---

## Root Cause Analysis

![root_cause_analysis](svg/courses/ai/developing-using-ai-short/09_workflows/root_cause_analysis.svg)

---

## Fix Implementation

AI assists with bug fixes:

```python
# AI suggests fix with explanation
class NotificationQueue:
    def __init__(self):
        self.retry_delays = [1, 5, 15, 60, 300]  # seconds

    async def send_with_retry(self, notification):
        """
        Fix: Implement exponential backoff for rate limits
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                result = await self.send(notification)
                return result
            except RateLimitError as e:
                if attempt == len(self.retry_delays) - 1:
                    # Final attempt failed
                    await self.move_to_dlq(notification)
                    raise
                logger.info(f"Rate limited, retry in {delay}s")
                await asyncio.sleep(delay)
```

---

## Code Maintenance: Dependency Updates

Managing dependencies safely:

```json
// AI analyzes and suggests updates
{
  "updates": {
    "safe": {
      "express": "4.18.0 → 4.18.2",
      "jest": "29.3.0 → 29.5.0"
    },
    "breaking": {
      "mongoose": "6.x → 7.x",
      "changes": [
        "- Removed callback support",
        "- Changed connection options",
        "- New strict mode default"
      ]
    },
    "security": {
      "lodash": "4.17.19 → 4.17.21",
      "severity": "high",
      "vulnerability": "Prototype pollution"
    }
  }
}
```

---

## Security Patches

Handling security updates:

```bash
#!/bin/bash
# Security patch automation

# 1. Check for vulnerabilities
npm audit --json > audit.json

# 2. AI analyzes critical issues
critical=$(jq '.metadata.vulnerabilities.critical' audit.json)

if [ "$critical" -gt 0 ]; then
  echo "⚠️ Critical vulnerabilities found"

  # 3. Create branch
  git checkout -b security/critical-updates

  # 4. Apply fixes
  npm audit fix --force

  # 5. Run tests
  npm test

  # 6. Create PR
  gh pr create --title "Security: Critical updates" \
               --body "$(npm audit)"
fi
```

---

## Technical Debt Reduction

Strategic refactoring:

```typescript
// AI identifies and prioritizes tech debt
interface TechDebt {
  id: string;
  type: 'code' | 'architecture' | 'dependency';
  severity: 'low' | 'medium' | 'high' | 'critical';
  effort: number; // story points
  impact: number; // 1-10
  description: string;
}

const debtItems: TechDebt[] = [
  {
    id: 'TD-001',
    type: 'architecture',
    severity: 'high',
    effort: 8,
    impact: 9,
    description: 'Monolithic user service needs splitting'
  },
  {
    id: 'TD-002',
    type: 'code',
    severity: 'medium',
    effort: 3,
    impact: 5,
    description: 'Duplicate validation logic in 5 files'
  }
];
```

---

## Release Preparation: Code Cleanup

![release_preparation_code_cleanup](svg/courses/ai/developing-using-ai-short/09_workflows/release_preparation_code_cleanup.svg)

---

## Documentation Updates

Preparing release docs:

```markdown
# AI generates release documentation

## Version 2.0.0 Release Notes

### 🎉 New Features
- Real-time notifications via WebSocket
- Bulk notification API
- Email template customization

### 🔧 Improvements
- 50% faster notification delivery
- Reduced memory usage by 30%
- Better error handling with retry logic

### 🐛 Bug Fixes
- Fixed race condition in queue processor
- Resolved timezone issues in scheduling

### 💔 Breaking Changes
- API response format changed (see migration guide)
- Required Node.js 18+
```

---

## Testing Completion

Final testing phases:

```javascript
// AI creates comprehensive test plan
const releaseTests = {
  unit: {
    coverage: "95%",
    suites: ["models", "services", "utils"],
    status: "✓ Passed"
  },
  integration: {
    apis: "All endpoints tested",
    database: "Migration tested",
    status: "✓ Passed"
  },
  e2e: {
    flows: ["signup", "notification", "preferences"],
    browsers: ["Chrome", "Firefox", "Safari"],
    status: "✓ Passed"
  },
  performance: {
    load: "1000 concurrent users",
    response: "p95 < 200ms",
    status: "✓ Passed"
  }
};
```

---

## Performance Monitoring

Real-time performance tracking:

![performance_monitoring](svg/courses/ai/developing-using-ai-short/09_workflows/performance_monitoring.svg)

---

## Incident Response

AI-assisted troubleshooting:

```python
# AI helps diagnose production issues
class IncidentResponder:
    def analyze_incident(self, alert):
        """AI analyzes incident and suggests actions"""

        analysis = {
            "severity": self.calculate_severity(alert),
            "affected_services": self.trace_dependencies(alert),
            "root_cause_hypothesis": [
                "Database connection pool exhausted",
                "Memory leak in notification service",
                "Third-party API rate limiting"
            ],
            "immediate_actions": [
                "Scale notification service +2 instances",
                "Clear Redis cache",
                "Enable circuit breaker for external API"
            ]
        }

        return self.prioritize_actions(analysis)
```

---

## Hot Fix Workflow

Rapid production fixes:

![hot_fix_workflow](svg/courses/ai/developing-using-ai-short/09_workflows/hot_fix_workflow.svg)

---

## Feature Flags

Progressive feature rollout:

```typescript
// AI manages feature flags
interface FeatureFlag {
  name: string;
  enabled: boolean;
  rolloutPercentage: number;
  targetGroups?: string[];
}

const featureFlags: FeatureFlag[] = [
  {
    name: "new-payment-flow",
    enabled: true,
    rolloutPercentage: 25,
    targetGroups: ["beta-users"]
  },
  {
    name: "ai-recommendations",
    enabled: true,
    rolloutPercentage: 100,
    targetGroups: ["all"]
  }
];

// AI suggests rollout strategy
function getRolloutPlan(feature: string) {
  return {
    week1: "5% internal users",
    week2: "25% beta users",
    week3: "50% all users",
    week4: "100% if metrics positive"
  };
}
```

---

## Multi-Environment Management

Managing multiple environments:

![multi_environment_management](svg/courses/ai/developing-using-ai-short/09_workflows/multi_environment_management.svg)

---

## Infrastructure Scaling

Auto-scaling configuration:

```yaml
# AI optimizes scaling policies
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-autoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service

  minReplicas: 3
  maxReplicas: 50

  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70

  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80

  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
```

---

## Success Metrics

Measuring project success:

![success_metrics](svg/courses/ai/developing-using-ai-short/09_workflows/success_metrics.svg)

---

## Lessons Learned Database

Building institutional knowledge:

```markdown
## Project: Shopping Cart Feature

### What Worked Well
- AI-generated test cases caught edge cases
- Incremental rollout prevented issues
- Feature flags allowed quick rollback

### Challenges
- Redis session management complexity
- Race conditions in concurrent updates

### Key Learnings
1. Always implement idempotency for cart operations
1. Use optimistic locking for inventory
1. Cache cart calculations aggressively

### AI Prompts That Worked
- "Generate test cases for cart edge cases"
- "Optimize cart query for 1000+ items"
- "Design cache invalidation strategy"
```

---

## Chapter Summary

**Key Takeaways**:

Real-world workflows require systematic approaches with AI

Complete coverage:
- Project lifecycle from init to deployment
- Feature development and bug fixing
- Performance monitoring and optimization
- Incident response and recovery
- Scaling and environment management

AI accelerates every aspect while maintaining quality and reliability
