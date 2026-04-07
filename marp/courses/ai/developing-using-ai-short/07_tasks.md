# Specialized Development Tasks

---

## Master Domain-Specific Development with AI

Leverage AI for specialized technical challenges across domains

This chapter covers:
1. Database development
1. Frontend development
1. Backend development
1. DevOps and automation
1. Mobile development

---

## Database Development: Schema Design

AI assists with optimal database structure:

```sql
-- You: "Design a schema for an e-commerce platform"
-- AI generates:

-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

CREATE INDEX idx_users_email ON users(email);

-- Products with Categories
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_price ON products(price);
```

---

## Query Optimization

![query_optimization](svg/courses/ai/developing-using-ai-short/07_tasks/query_optimization.svg)

---

## Migration Scripts

AI generates safe database migrations:

```python
# AI creates migration with rollback:

def upgrade():
    """Apply migration - add preferences"""
    op.create_table(
        'user_preferences',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('theme', sa.String(20), default='light'),
        sa.Column('notifications_enabled', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now())
    )

    op.create_foreign_key(
        'fk_preferences_user',
        'user_preferences', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

    op.create_index('idx_preferences_user', 'user_preferences', ['user_id'])

def downgrade():
    """Rollback migration - remove preferences"""
    op.drop_index('idx_preferences_user', 'user_preferences')
    op.drop_table('user_preferences')
```

---

## Performance Tuning

Database optimization strategies:

```python
class DatabaseOptimizer:
    def implement_connection_pooling(self):
        """Connection pool configuration"""
        from sqlalchemy.pool import QueuePool

        engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=20,          # Number of connections
            max_overflow=40,       # Maximum overflow connections
            pool_timeout=30,       # Timeout in seconds
            pool_recycle=1800,     # Recycle connections after 30 min
            pool_pre_ping=True     # Test connections before use
        )
        return engine

    def optimize_orm_queries(self):
        """ORM-specific optimizations"""
        # Eager loading to prevent N+1
        users = db.query(User)\
            .options(joinedload(User.orders))\
            .options(selectinload(User.preferences))\
            .all()

        # Bulk operations
        db.bulk_insert_mappings(User, user_data)

        # Query only needed columns
        results = db.query(User.id, User.email)\
            .filter(User.active == True)\
            .limit(100)\
            .all()
```

---

## Frontend Development: Component Generation

AI creates reusable components:

```typescript
// You: "Create a data table component with sorting and pagination"
interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  itemsPerPage?: number;
  searchable?: boolean;
}

export function DataTable<T extends Record<string, any>>({
  data,
  columns,
  itemsPerPage = 10,
  searchable = true
}: DataTableProps<T>) {
  const [currentPage, setCurrentPage] = useState(1);
  const [sortConfig, setSortConfig] = useState<{
    key: keyof T | null;
    direction: 'asc' | 'desc';
  }>({ key: null, direction: 'asc' });
  const [searchTerm, setSearchTerm] = useState('');

  // Filter data based on search
  const filteredData = useMemo(() => {
    if (!searchTerm) return data;
    return data.filter(item =>
      Object.values(item).some(value =>
        String(value).toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
  }, [data, searchTerm]);

  // Sort and paginate
  const sortedData = useMemo(() => {
    if (!sortConfig.key) return filteredData;
    return [...filteredData].sort((a, b) => {
      const aVal = a[sortConfig.key!];
      const bVal = b[sortConfig.key!];
      if (aVal < bVal) return sortConfig.direction === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortConfig.direction === 'asc' ? 1 : -1;
      return 0;
    });
  }, [filteredData, sortConfig]);

  return (
    <div className="data-table">
      {/* Table implementation */}
    </div>
  );
}
```

---

## Responsive Design

AI creates responsive layouts:

```css
/* Mobile-first responsive grid */
.container {
  width: 100%;
  padding: 0 1rem;
  margin: 0 auto;
}

@media (min-width: 640px) {
  .container { max-width: 640px; }
}

@media (min-width: 1024px) {
  .container { max-width: 1024px; }
}

/* Flexible grid with CSS Grid */
.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

/* Responsive typography with clamp() */
h1 {
  font-size: clamp(1.5rem, 4vw, 3rem);
  line-height: 1.2;
}

/* Container queries for component-level responsiveness */
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: flex;
    gap: 1rem;
  }
}
```

---

## Accessibility Improvements

Making interfaces accessible:

```jsx
const AccessibleForm = () => {
  const [errors, setErrors] = useState({});

  return (
    <form aria-label="Contact form" onSubmit={handleSubmit}>
      {/* Screen reader announcements */}
      <div role="status" aria-live="polite" aria-atomic="true" className="sr-only">
        {announcement}
      </div>

      {/* Accessible input with label */}
      <div className="form-group">
        <label htmlFor="email-input">
          Email Address
          <span aria-label="required">*</span>
        </label>
        <input
          id="email-input"
          type="email"
          name="email"
          required
          aria-required="true"
          aria-invalid={errors.email ? 'true' : 'false'}
          aria-describedby={errors.email ? 'email-error' : 'email-hint'}
        />
        {errors.email && (
          <span id="email-error" role="alert" className="error">
            {errors.email}
          </span>
        )}
      </div>

      {/* Accessible button with loading state */}
      <button
        type="submit"
        disabled={isLoading}
        aria-busy={isLoading}
        aria-label={isLoading ? 'Submitting form' : 'Submit form'}
      >
        {isLoading ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
};
```

---

## State Management

Frontend state solutions:

```typescript
// AI implements state management patterns:

interface AppState {
  user: User | null;
  theme: 'light' | 'dark';
  notifications: Notification[];
  isLoading: boolean;
}

type Action =
  | { type: 'SET_USER'; payload: User }
  | { type: 'TOGGLE_THEME' }
  | { type: 'ADD_NOTIFICATION'; payload: Notification }
  | { type: 'SET_LOADING'; payload: boolean };

const AppContext = React.createContext<{
  state: AppState;
  dispatch: React.Dispatch<Action>;
} | null>(null);

const appReducer = (state: AppState, action: Action): AppState => {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'TOGGLE_THEME':
      return { ...state, theme: state.theme === 'light' ? 'dark' : 'light' };
    case 'ADD_NOTIFICATION':
      return { ...state, notifications: [...state.notifications, action.payload] };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    default:
      return state;
  }
};
```

---

## Backend Development: API Design

RESTful and GraphQL API patterns:

```javascript
// RESTful API with Express
const express = require('express');
const router = express.Router();

// Resource-based routing
router.route('/api/v1/users')
  .get(validateQuery, paginate, getUsers)
  .post(validateBody, authenticate, createUser);

router.route('/api/v1/users/:id')
  .get(validateParams, getUser)
  .put(validateBody, authorize, updateUser)
  .delete(authorize, softDeleteUser);

// GraphQL alternative
const typeDefs = `
  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
  }

  type Query {
    users(limit: Int, offset: Int): [User!]!
    user(id: ID!): User
  }

  type Mutation {
    createUser(input: UserInput!): User!
    updateUser(id: ID!, input: UserInput!): User!
  }
`;
```

---

## Authentication/Authorization

![authentication_authorization](svg/courses/ai/developing-using-ai-short/07_tasks/authentication_authorization.svg)

---

## Data Validation

Comprehensive validation layers:

```typescript
import { z } from 'zod';

// Schema definitions
const UserSchema = z.object({
  email: z.string().email().toLowerCase(),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[0-9]/, 'Must contain number'),
  age: z.number().min(13).max(120),
  role: z.enum(['user', 'admin', 'moderator'])
});

// Validation middleware
const validate = (schema: z.ZodSchema) => {
  return async (req, res, next) => {
    try {
      req.body = await schema.parseAsync(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          errors: error.errors.map(e => ({
            field: e.path.join('.'),
            message: e.message
          }))
        });
      }
      next(error);
    }
  };
};
```

---

## Error Handling

Robust error management system:

```javascript
class AppError extends Error {
  constructor(message, statusCode, isOperational = true) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = isOperational;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Global error handler
const errorHandler = (err, req, res, next) => {
  let error = { ...err };

  // Log error
  logger.error({
    error: err,
    request: req.url,
    method: req.method,
    user: req.user?.id
  });

  // Mongoose bad ObjectId
  if (err.name === 'CastError') {
    error = new AppError('Resource not found', 404);
  }

  // Mongoose duplicate key
  if (err.code === 11000) {
    const field = Object.keys(err.keyValue)[0];
    error = new AppError(`${field} already exists`, 400);
  }

  res.status(error.statusCode || 500).json({
    success: false,
    error: error.message || 'Server Error'
  });
};
```

---

## DevOps: CI/CD Pipeline

GitHub Actions workflow:

```yaml
name: Production Deployment

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - uses: codecov/codecov-action@v3

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'

    steps:
      - uses: actions/checkout@v3
      - uses: docker/setup-buildx-action@v2
      - uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/app app=ghcr.io/${{ github.repository }}:${{ github.sha }}
          kubectl rollout status deployment/app
```

---

## Infrastructure as Code

Terraform configuration:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# EKS Cluster
module "eks" {
  source = "terraform-aws-modules/eks/aws"

  cluster_name    = "${var.project_name}-cluster"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    general = {
      desired_size = 3
      min_size     = 2
      max_size     = 10
      instance_types = ["t3.medium"]
    }
  }

  enable_irsa = true
}

# RDS Database
resource "aws_db_instance" "postgres" {
  identifier = "${var.project_name}-db"

  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.medium"

  allocated_storage = 100
  storage_encrypted = true

  backup_retention_period = 30
  deletion_protection = true
}
```

---

## Mobile Development: Cross-Platform

![mobile_development_cross_platform](svg/courses/ai/developing-using-ai-short/07_tasks/mobile_development_cross_platform.svg)

---

## Platform-Specific Features

React Native with platform code:

```typescript
import { Platform, StyleSheet, Vibration } from 'react-native';
import * as Haptics from 'expo-haptics';
import * as Notifications from 'expo-notifications';

class PlatformFeatures {
  // Platform-specific styling
  static getStyles() {
    return StyleSheet.create({
      container: {
        ...Platform.select({
          ios: {
            paddingTop: 20,
            shadowColor: '#000',
            shadowOffset: { width: 0, height: 2 },
            shadowOpacity: 0.1,
          },
          android: {
            paddingTop: 25,
            elevation: 4,
          },
        }),
      },
    });
  }

  // Push notifications
  static async setupNotifications() {
    const { status } = await Notifications.requestPermissionsAsync();

    if (status !== 'granted') {
      return;
    }

    // Platform-specific configuration
    if (Platform.OS === 'android') {
      Notifications.setNotificationChannelAsync('default', {
        name: 'default',
        importance: Notifications.AndroidImportance.MAX,
      });
    }

    return (await Notifications.getExpoPushTokenAsync()).data;
  }
}
```

---

## Microservices Architecture

![microservices_architecture](svg/courses/ai/developing-using-ai-short/07_tasks/microservices_architecture.svg)

---

## Serverless Development

Lambda function patterns:

```python
import json
import boto3

def lambda_handler(event, context):
    """AWS Lambda function for processing orders"""
    try:
        body = json.loads(event.get('body', '{}'))

        if not body.get('orderId'):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'orderId required'})
            }

        # Process order
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('orders')

        response = table.update_item(
            Key={'orderId': body['orderId']},
            UpdateExpression='SET #status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': 'processed'},
            ReturnValues='ALL_NEW'
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Order processed successfully',
                'order': response['Attributes']
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

---

## Architecture at Scale

Scaling strategies for growth:

```yaml
# Horizontal scaling with Kubernetes
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  minReplicas: 3
  maxReplicas: 100
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      selectPolicy: Max
```

---

## Chapter Summary

**Key Takeaways**:

AI accelerates specialized development across all domains

Completed coverage of:
- Database: Schema design, optimization, migrations
- Frontend: Components, accessibility, state management
- Backend: APIs, validation, error handling
- DevOps: CI/CD, infrastructure as code
- Mobile: Cross-platform and native features
- Architecture: Microservices, serverless, scaling

Each specialization leverages AI's deep domain knowledge
