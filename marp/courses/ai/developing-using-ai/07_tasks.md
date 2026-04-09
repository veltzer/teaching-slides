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

## The Specialization Advantage

![the_specialization_advantage](svg/courses/ai/developing-using-ai/07_tasks/the_specialization_advantage.svg)

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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = true;

-- Products with Categories
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    parent_id INTEGER REFERENCES categories(id),
    path TEXT, -- Materialized path for hierarchy
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    category_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_price ON products(price);
```

---

## Query Optimization

![query_optimization](svg/courses/ai/developing-using-ai/07_tasks/query_optimization.svg)

---

## Migration Scripts

AI generates safe database migrations:

```python
# AI creates migration with rollback:

"""
Migration: Add user preferences table
Version: 20240315_add_user_preferences
"""

def upgrade():
    """
    Apply migration - add preferences
    """
    op.create_table(
        'user_preferences',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('theme', sa.String(20), default='light'),
        sa.Column('language', sa.String(5), default='en'),
        sa.Column('notifications_enabled', sa.Boolean(), default=True),
        sa.Column('timezone', sa.String(50), default='UTC'),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now())
    )

    # Add foreign key constraint
    op.create_foreign_key(
        'fk_preferences_user',
        'user_preferences', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

    # Add indexes for performance
    op.create_index('idx_preferences_user', 'user_preferences', ['user_id'])

    # Migrate existing users
    op.execute("""
        INSERT INTO user_preferences (user_id)
        SELECT id FROM users
        WHERE id NOT IN (SELECT user_id FROM user_preferences)
    """)

def downgrade():
    """
    Rollback migration - remove preferences
    """
    op.drop_index('idx_preferences_user', 'user_preferences')
    op.drop_constraint('fk_preferences_user', 'user_preferences')
    op.drop_table('user_preferences')
```

---

## Index Strategies

Intelligent indexing decisions:

```sql
-- AI analyzes query patterns and suggests indexes:

-- Query Pattern Analysis
-- Most common queries:
-- 1. SELECT * FROM orders WHERE user_id = ? AND status = 'active'
-- 2. SELECT * FROM products WHERE category_id = ? ORDER BY price
-- 3. SELECT * FROM users WHERE email = ? AND is_active = true

-- Recommended Indexes:

-- Composite index for orders
CREATE INDEX idx_orders_user_status
ON orders(user_id, status)
WHERE status = 'active'; -- Partial index for common filter

-- Covering index for products
CREATE INDEX idx_products_category_price
ON products(category_id, price)
INCLUDE (name, stock_quantity); -- Include frequently selected columns

-- Unique partial index for users
CREATE UNIQUE INDEX idx_users_email_active
ON users(email)
WHERE is_active = true; -- Ensure unique active emails

-- JSON index for metadata
CREATE INDEX idx_products_metadata
ON products USING GIN (metadata jsonb_path_ops); -- For JSONB queries

-- Full-text search index
CREATE INDEX idx_products_search
ON products USING GIN (to_tsvector('english', name || ' ' || description));

-- Monitor index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

---

## Data Modeling

![data_modeling](svg/courses/ai/developing-using-ai/07_tasks/data_modeling.svg)

---

## Performance Tuning

Database optimization strategies:

```python
# AI suggests performance improvements:

class DatabaseOptimizer:
    def analyze_slow_queries(self):
        """
        Identify and optimize slow queries
        """
        slow_queries = """
        SELECT
            query,
            calls,
            mean_exec_time,
            total_exec_time
        FROM pg_stat_statements
        WHERE mean_exec_time > 100  -- queries over 100ms
        ORDER BY mean_exec_time DESC
        LIMIT 10;
        """

        optimization_strategies = {
            "missing_index": self.suggest_index,
            "full_table_scan": self.add_where_clause,
            "n_plus_one": self.batch_queries,
            "no_limit": self.add_pagination,
            "select_star": self.specify_columns,
            "no_caching": self.implement_cache
        }

        return optimization_strategies

    def implement_connection_pooling(self):
        """
        Connection pool configuration
        """
        from sqlalchemy.pool import QueuePool

        engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=20,          # Number of connections
            max_overflow=40,       # Maximum overflow connections
            pool_timeout=30,       # Timeout in seconds
            pool_recycle=1800,     # Recycle connections after 30 min
            pool_pre_ping=True,    # Test connections before use
            echo_pool=True         # Log pool checkouts/checkins
        )

        return engine

    def optimize_orm_queries(self):
        """
        ORM-specific optimizations
        """
        # Eager loading to prevent N+1
        users = db.query(User)\
            .options(joinedload(User.orders))\
            .options(selectinload(User.preferences))\
            .all()

        # Bulk operations
        db.bulk_insert_mappings(User, user_data)
        db.bulk_update_mappings(User, updates)

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
// You: "Create a data table component with sorting, filtering, and pagination"
// AI generates:

import React, { useState, useMemo } from 'react';
import { ChevronUp, ChevronDown, Search } from 'lucide-react';

interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  itemsPerPage?: number;
  searchable?: boolean;
  className?: string;
}

interface Column<T> {
  key: keyof T;
  header: string;
  sortable?: boolean;
  render?: (value: T[keyof T], item: T) => React.ReactNode;
  width?: string;
}

export function DataTable<T extends Record<string, any>>({
  data,
  columns,
  itemsPerPage = 10,
  searchable = true,
  className = ''
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

  // Sort data
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

  // Paginate data
  const paginatedData = useMemo(() => {
    const start = (currentPage - 1) * itemsPerPage;
    return sortedData.slice(start, start + itemsPerPage);
  }, [sortedData, currentPage, itemsPerPage]);

  const totalPages = Math.ceil(sortedData.length / itemsPerPage);

  const handleSort = (key: keyof T) => {
    setSortConfig(prev => ({
      key,
      direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc'
    }));
  };

  return (
    <div className={`data-table ${className}`}>
      {searchable && (
        <div className="table-search">
          <Search size={20} />
          <input
            type="text"
            placeholder="Search..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      )}

      <table>
        <thead>
          <tr>
            {columns.map(column => (
              <th
                key={String(column.key)}
                style={{ width: column.width }}
                onClick={() => column.sortable && handleSort(column.key)}
                className={column.sortable ? 'sortable' : ''}
              >
                {column.header}
                {column.sortable && sortConfig.key === column.key && (
                  sortConfig.direction === 'asc' ? <ChevronUp /> : <ChevronDown />
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {paginatedData.map((item, index) => (
            <tr key={index}>
              {columns.map(column => (
                <td key={String(column.key)}>
                  {column.render
                    ? column.render(item[column.key], item)
                    : item[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      <div className="pagination">
        <button
          onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
          disabled={currentPage === 1}
        >
          Previous
        </button>
        <span>Page {currentPage} of {totalPages}</span>
        <button
          onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
          disabled={currentPage === totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
}
```

---

## Styling Assistance

![styling_assistance](svg/courses/ai/developing-using-ai/07_tasks/styling_assistance.svg)

---

## Responsive Design

AI creates responsive layouts:

```css
/* AI generates responsive grid system */

/* Mobile-first responsive grid */
.container {
  width: 100%;
  padding: 0 1rem;
  margin: 0 auto;
}

/* Breakpoint system */
/* Mobile: 0-639px (default) */
/* Tablet: 640px-1023px */
/* Desktop: 1024px-1279px */
/* Large: 1280px+ */

@media (min-width: 640px) {
  .container { max-width: 640px; }
}

@media (min-width: 1024px) {
  .container { max-width: 1024px; }
}

@media (min-width: 1280px) {
  .container { max-width: 1280px; }
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

p {
  font-size: clamp(1rem, 2vw, 1.25rem);
  line-height: 1.6;
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

  .card-image {
    width: 40%;
  }
}

/* Responsive utilities */
.hide-mobile { display: none; }
.hide-tablet { display: block; }
.hide-desktop { display: block; }

@media (min-width: 640px) {
  .hide-mobile { display: block; }
  .hide-tablet { display: none; }
}

@media (min-width: 1024px) {
  .hide-tablet { display: block; }
  .hide-desktop { display: none; }
}
```

---

## Accessibility Improvements

Making interfaces accessible:

```jsx
// AI adds accessibility features:

const AccessibleForm = () => {
  const [errors, setErrors] = useState({});
  const [announcement, setAnnouncement] = useState('');

  return (
    <form
      aria-label="Contact form"
      onSubmit={handleSubmit}
    >
      {/* Screen reader announcements */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
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
        <span id="email-hint" className="hint">
          We'll never share your email
        </span>
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
        {isLoading ? (
          <>
            <span className="spinner" aria-hidden="true"></span>
            <span>Submitting...</span>
          </>
        ) : (
          'Submit'
        )}
      </button>

      {/* Skip link for keyboard navigation */}
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      {/* Focus trap for modals */}
      <FocusTrap active={isModalOpen}>
        <Modal />
      </FocusTrap>
    </form>
  );
};
```

---

## Animation Creation

![animation_creation](svg/courses/ai/developing-using-ai/07_tasks/animation_creation.svg)

---

## State Management

Frontend state solutions:

```typescript
// AI implements state management patterns:

// 1. Context API with useReducer
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
```

---

## Script Generation

AI creates automation scripts:

```bash
#!/bin/bash
# AI-generated deployment script with error handling

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
readonly APP_NAME="my-app"
readonly DEPLOY_ENV="${1:-production}"
readonly BACKUP_DIR="/var/backups/${APP_NAME}"
readonly LOG_FILE="/var/log/${APP_NAME}/deploy.log"

# Color output for better readability
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error_exit() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit 1
}

# Pre-deployment checks
pre_deploy_checks() {
    log "Running pre-deployment checks..."

    # Check disk space
    available_space=$(df / | awk 'NR==2 {print $4}')
    if [ "$available_space" -lt 1000000 ]; then
        error_exit "Insufficient disk space"
    fi

    # Check if services are running
    systemctl is-active --quiet nginx || error_exit "Nginx is not running"
    systemctl is-active --quiet postgresql || error_exit "PostgreSQL is not running"

    # Verify environment variables
    [ -z "${DATABASE_URL:-}" ] && error_exit "DATABASE_URL not set"
    [ -z "${API_KEY:-}" ] && error_exit "API_KEY not set"

    log "Pre-deployment checks passed ✓"
}

# Backup current deployment
backup_current() {
    log "Creating backup..."

    local backup_name="${APP_NAME}_$(date +'%Y%m%d_%H%M%S')"
    mkdir -p "$BACKUP_DIR"

    # Backup application files
    tar -czf "${BACKUP_DIR}/${backup_name}_app.tar.gz" \
        --exclude='node_modules' \
        --exclude='*.log' \
        /var/www/${APP_NAME}

    # Backup database
    pg_dump "$DATABASE_URL" | gzip > "${BACKUP_DIR}/${backup_name}_db.sql.gz"

    # Keep only last 5 backups
    ls -t ${BACKUP_DIR}/*.tar.gz | tail -n +6 | xargs -r rm

    log "Backup completed: ${backup_name}"
}

# Deploy new version
deploy() {
    log "Starting deployment for ${DEPLOY_ENV}..."

    # Pull latest code
    cd /var/www/${APP_NAME}
    git fetch origin
    git reset --hard origin/${DEPLOY_ENV}

    # Install dependencies
    npm ci --production

    # Run database migrations
    npm run migrate:up

    # Build assets
    npm run build

    # Restart services
    pm2 reload ecosystem.config.js --env ${DEPLOY_ENV}

    # Clear cache
    redis-cli FLUSHDB

    log "Deployment completed successfully ✅"
}

# Health check
health_check() {
    log "Running health checks..."

    local max_attempts=10
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if curl -f -s -o /dev/null "http://localhost:3000/health"; then
            log "Health check passed ✓"
            return 0
        fi

        attempt=$((attempt + 1))
        log "Health check attempt ${attempt}/${max_attempts} failed, retrying..."
        sleep 3
    done

    error_exit "Health check failed after ${max_attempts} attempts"
}

# Main execution
main() {
    log "=== Starting deployment process ==="

    pre_deploy_checks
    backup_current
    deploy
    health_check

    log "=== Deployment completed successfully ==="

    # Send notification
    curl -X POST "$SLACK_WEBHOOK" \
        -H 'Content-Type: application/json' \
        -d "{\"text\":\"✅ ${APP_NAME} deployed to ${DEPLOY_ENV}\"}"
}

# Run with error handling
trap 'error_exit "Deployment failed at line $LINENO"' ERR
main "$@"
```

---

## Configuration Files

![configuration_files](svg/courses/ai/developing-using-ai/07_tasks/configuration_files.svg)

---

## CI/CD Pipelines

GitHub Actions workflow:

```yaml
# AI generates comprehensive CI/CD pipeline:

name: Production Deployment

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '18'
  DOCKER_REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        test-suite: [unit, integration, e2e]

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ${{ matrix.test-suite }} tests
        run: npm run test:${{ matrix.test-suite }}
        env:
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}

      - name: Upload coverage
        if: matrix.test-suite == 'unit'
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run security audit
        run: npm audit --audit-level=moderate

      - name: Run SAST scan
        uses: github/super-linter@v4
        env:
          DEFAULT_BRANCH: main
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Dependency vulnerability scan
        uses: snyk/actions/node@master
        with:
          args: --severity-threshold=high

  build-and-push:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    if: github.event_name == 'push'

    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.DOCKER_REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:latest
            ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            BUILD_VERSION=${{ github.sha }}
            BUILD_TIME=${{ github.event.head_commit.timestamp }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v4
        with:
          manifests: |
            k8s/deployment.yaml
            k8s/service.yaml
          images: |
            ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

      - name: Verify deployment
        run: |
          kubectl rollout status deployment/app-deployment
          kubectl get services

      - name: Run smoke tests
        run: |
          ENDPOINT=$(kubectl get service app-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
          curl -f http://${ENDPOINT}/health || exit 1
```

---

## Deployment Scripts

Kubernetes deployment configuration:

```yaml
# AI creates K8s manifests:

apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  labels:
    app: myapp
    environment: production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      containers:
      - name: app
        image: myapp:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 3000
          name: http
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: connection-string
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5

      # Init container for database migrations
      initContainers:
      - name: migrate
        image: myapp:latest
        command: ['npm', 'run', 'migrate:up']
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: connection-string

      # Pod disruption budget
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - myapp
              topologyKey: kubernetes.io/hostname

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app-deployment
  minReplicas: 3
  maxReplicas: 10
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
```

---

## Monitoring Setup

![monitoring_setup](svg/courses/ai/developing-using-ai/07_tasks/monitoring_setup.svg)

---

## Infrastructure as Code

Terraform configuration:

```hcl
# AI generates Terraform infrastructure:

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "terraform-state-bucket"
    key    = "production/terraform.tfstate"
    region = "us-west-2"
    encrypt = true
    dynamodb_table = "terraform-locks"
  }
}

# VPC Configuration
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "${var.project_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-west-2a", "us-west-2b", "us-west-2c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = true
  enable_dns_hostnames = true

  tags = local.common_tags
}

# EKS Cluster
module "eks" {
  source = "terraform-aws-modules/eks/aws"

  cluster_name    = "${var.project_name}-cluster"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Node groups
  eks_managed_node_groups = {
    general = {
      desired_size = 3
      min_size     = 2
      max_size     = 10

      instance_types = ["t3.medium"]

      k8s_labels = {
        Environment = "production"
        NodeType    = "general"
      }
    }

    spot = {
      desired_size = 2
      min_size     = 1
      max_size     = 5

      capacity_type = "SPOT"
      instance_types = ["t3.medium", "t3.large"]

      taints = [{
        key    = "spot"
        value  = "true"
        effect = "NO_SCHEDULE"
      }]
    }
  }

  # Enable IRSA
  enable_irsa = true

  # Cluster addons
  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    aws-ebs-csi-driver = {
      most_recent = true
    }
  }
}

# RDS Database
resource "aws_db_instance" "postgres" {
  identifier = "${var.project_name}-db"

  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.medium"

  allocated_storage     = 100
  storage_encrypted     = true
  storage_type         = "gp3"

  db_name  = var.db_name
  username = var.db_username
  password = random_password.db_password.result

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  deletion_protection = true
  skip_final_snapshot = false

  performance_insights_enabled = true
  monitoring_interval         = 60

  tags = local.common_tags
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "${var.project_name}-cache"
  engine              = "redis"
  node_type           = "cache.t3.micro"
  num_cache_nodes     = 1
  parameter_group_name = "default.redis7"
  port                = 6379

  snapshot_retention_limit = 5
  snapshot_window         = "03:00-05:00"

  subnet_group_name = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.redis.id]

  tags = local.common_tags
}
```

---

## Mobile Development: Cross-Platform Code

![mobile_development_cross_platform_code](svg/courses/ai/developing-using-ai/07_tasks/mobile_development_cross_platform_code.svg)

---

## Platform-Specific Features

React Native with platform code:

```typescript
// AI implements platform-specific features:

import {
  Platform,
  StyleSheet,
  Alert,
  Vibration,
  Share,
  Linking
} from 'react-native';
import * as Haptics from 'expo-haptics';
import * as Notifications from 'expo-notifications';
import * as Location from 'expo-location';

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
            shadowRadius: 4,
          },
          android: {
            paddingTop: 25,
            elevation: 4,
          },
          web: {
            paddingTop: 10,
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          },
        }),
      },
    });
  }

  // Haptic feedback
  static async triggerHaptic(type: 'light' | 'medium' | 'heavy') {
    if (Platform.OS === 'ios') {
      await Haptics.impactAsync(
        type === 'light' ? Haptics.ImpactFeedbackStyle.Light :
        type === 'medium' ? Haptics.ImpactFeedbackStyle.Medium :
        Haptics.ImpactFeedbackStyle.Heavy
      );
    } else if (Platform.OS === 'android') {
      Vibration.vibrate(
        type === 'light' ? 10 :
        type === 'medium' ? 20 : 40
      );
    }
  }

  // Push notifications
  static async setupNotifications() {
    const { status: existingStatus } =
      await Notifications.getPermissionsAsync();

    let finalStatus = existingStatus;

    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }

    if (finalStatus !== 'granted') {
      Alert.alert('Permission required', 'Please enable notifications');
      return;
    }

    // Configure notification handler
    Notifications.setNotificationHandler({
      handleNotification: async () => ({
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: true,
      }),
    });

    // Get push token
    const token = (await Notifications.getExpoPushTokenAsync()).data;

    // Platform-specific configuration
    if (Platform.OS === 'android') {
      Notifications.setNotificationChannelAsync('default', {
        name: 'default',
        importance: Notifications.AndroidImportance.MAX,
        vibrationPattern: [0, 250, 250, 250],
        lightColor: '#FF231F7C',
      });
    }

    return token;
  }

  // Location services
  static async getCurrentLocation() {
    const { status } = await Location.requestForegroundPermissionsAsync();

    if (status !== 'granted') {
      throw new Error('Location permission denied');
    }

    const location = await Location.getCurrentPositionAsync({
      accuracy: Platform.OS === 'ios'
        ? Location.Accuracy.BestForNavigation
        : Location.Accuracy.High,
    });

    return {
      latitude: location.coords.latitude,
      longitude: location.coords.longitude,
      accuracy: location.coords.accuracy,
    };
  }

  // Deep linking
  static async openURL(url: string) {
    const supported = await Linking.canOpenURL(url);

    if (supported) {
      await Linking.openURL(url);
    } else {
      Alert.alert('Error', `Cannot open URL: ${url}`);
    }
  }

  // Share functionality
  static async share(content: { message: string; url?: string }) {
    try {
      const result = await Share.share({
        message: content.message,
        url: content.url,
        title: Platform.OS === 'ios' ? 'Share' : undefined,
      });

      if (result.action === Share.sharedAction) {
        return { shared: true, platform: result.activityType };
      }

      return { shared: false };
    } catch (error) {
      Alert.alert('Error', 'Failed to share content');
      throw error;
    }
  }
}
```

---

## UI/UX Patterns

Mobile-specific UI patterns:

```jsx
// AI creates mobile UI components:

import React, { useRef, useState } from 'react';
import {
  View,
  ScrollView,
  FlatList,
  RefreshControl,
  TouchableOpacity,
  Animated,
  PanResponder,
  Dimensions,
} from 'react-native';

const { width: screenWidth } = Dimensions.get('window');
```

## Backend Development: API Design

RESTful and GraphQL API patterns:

```javascript
// AI generates comprehensive API structure:

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

## Business Logic Implementation

Clean architecture patterns:

```python
# AI implements domain-driven design:

class OrderService:
    """Business logic layer - framework agnostic"""

    def __init__(self, order_repo, payment_gateway, notification_service):
        self.order_repo = order_repo
        self.payment = payment_gateway
        self.notifier = notification_service

    async def place_order(self, customer_id: str, items: List[OrderItem]) -> Order:
        # Business rules validation
        if not items:
            raise BusinessRuleViolation("Order must contain items")

        total = self._calculate_total(items)

        if total > 10000:
            require_approval = True

        # Create order aggregate
        order = Order(
            customer_id=customer_id,
            items=items,
            total=total,
            status=OrderStatus.PENDING
        )

        # Process payment
        payment_result = await self.payment.charge(customer_id, total)

        if payment_result.success:
            order.mark_as_paid(payment_result.transaction_id)
            await self.order_repo.save(order)
            await self.notifier.send_confirmation(order)
        else:
            order.mark_as_failed(payment_result.error)
            raise PaymentFailedException(payment_result.error)

        return order
```

---

## Authentication/Authorization

![authentication_authorization](svg/courses/ai/developing-using-ai/07_tasks/authentication_authorization.svg)

---

## Data Validation

Comprehensive validation layers:

```typescript
// AI creates validation system:

import { z } from 'zod';

// Schema definitions
const UserSchema = z.object({
  email: z.string().email().toLowerCase(),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[a-z]/, 'Must contain lowercase')
    .regex(/[0-9]/, 'Must contain number')
    .regex(/[^A-Za-z0-9]/, 'Must contain special character'),
  age: z.number().min(13).max(120),
  role: z.enum(['user', 'admin', 'moderator']),
  preferences: z.object({
    theme: z.enum(['light', 'dark']).optional(),
    notifications: z.boolean().default(true),
  }).optional(),
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
// AI implements error handling:

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
  error.message = err.message;

  // Log error
  logger.error({
    error: err,
    request: req.url,
    method: req.method,
    ip: req.ip,
    user: req.user?.id
  });

  // Mongoose bad ObjectId
  if (err.name === 'CastError') {
    const message = 'Resource not found';
    error = new AppError(message, 404);
  }

  // Mongoose duplicate key
  if (err.code === 11000) {
    const field = Object.keys(err.keyValue)[0];
    const message = `${field} already exists`;
    error = new AppError(message, 400);
  }

  // Mongoose validation error
  if (err.name === 'ValidationError') {
    const message = Object.values(err.errors).map(val => val.message).join(', ');
    error = new AppError(message, 400);
  }

  res.status(error.statusCode || 500).json({
    success: false,
    error: error.message || 'Server Error',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};
```

---

## Performance Optimization

Backend optimization strategies:

![performance_optimization](svg/courses/ai/developing-using-ai/07_tasks/performance_optimization.svg)

---

## DevOps and Automation

Infrastructure automation overview:

```yaml
# AI creates Docker Compose setup:

version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        NODE_ENV: production
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@postgres:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - app

volumes:
  postgres_data:
  redis_data:
```

---

## Native Integrations

Bridging to native mobile features:

```kotlin
// Android Kotlin module:
class BiometricAuthModule(reactContext: ReactApplicationContext) :
    ReactContextBaseJavaModule(reactContext) {

    override fun getName() = "BiometricAuth"

    @ReactMethod
    fun authenticate(reason: String, promise: Promise) {
        val executor = ContextCompat.getMainExecutor(reactApplicationContext)
        val biometricPrompt = BiometricPrompt(
            currentActivity as FragmentActivity,
            executor,
            object : BiometricPrompt.AuthenticationCallback() {
                override fun onAuthenticationSucceeded(
                    result: BiometricPrompt.AuthenticationResult
                ) {
                    promise.resolve(true)
                }

                override fun onAuthenticationError(
                    errorCode: Int,
                    errString: CharSequence
                ) {
                    promise.reject("AUTH_ERROR", errString.toString())
                }
            }
        )

        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Authentication Required")
            .setSubtitle(reason)
            .setNegativeButtonText("Cancel")
            .build()

        biometricPrompt.authenticate(promptInfo)
    }
}
```

---

## Testing Strategies

Comprehensive testing with AI:

```python
# AI generates test suites:

import pytest
from unittest.mock import Mock, patch
import asyncio

class TestOrderService:
    @pytest.fixture
    def service(self):
        mock_repo = Mock()
        mock_payment = Mock()
        mock_notifier = Mock()
        return OrderService(mock_repo, mock_payment, mock_notifier)

    @pytest.mark.asyncio
    async def test_successful_order_placement(self, service):
        # Arrange
        customer_id = "customer123"
        items = [OrderItem(product_id="prod1", quantity=2, price=50.0)]

        service.payment.charge = Mock(return_value=asyncio.coroutine(
            lambda: PaymentResult(success=True, transaction_id="txn123")
        )())

        # Act
        order = await service.place_order(customer_id, items)

        # Assert
        assert order.status == OrderStatus.PAID
        assert order.total == 100.0
        service.order_repo.save.assert_called_once()
        service.notifier.send_confirmation.assert_called_once()

    @pytest.mark.asyncio
    async def test_order_fails_with_empty_items(self, service):
        with pytest.raises(BusinessRuleViolation) as exc:
            await service.place_order("customer123", [])
        assert "must contain items" in str(exc.value)
```

---

## Documentation Generation

Auto-generated API documentation:

![documentation_generation](svg/courses/ai/developing-using-ai/07_tasks/documentation_generation.svg)

---

## Security Best Practices

Security implementation patterns:

```javascript
// AI implements security measures:

const securityMiddleware = {
  // Rate limiting
  rateLimiter: rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
    message: 'Too many requests'
  }),

  // CORS configuration
  cors: cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization']
  }),

  // Helmet for security headers
  helmet: helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", "data:", "https:"],
      },
    },
  }),

  // Input sanitization
  sanitize: (req, res, next) => {
    req.body = sanitizeInput(req.body);
    req.query = sanitizeInput(req.query);
    req.params = sanitizeInput(req.params);
    next();
  },

  // SQL injection prevention
  preventSQLi: (query) => {
    return query.replace(/['";\\]/g, '');
  }
};
```

---

## Microservices Architecture

Service communication patterns:

![microservices_architecture](svg/courses/ai/developing-using-ai/07_tasks/microservices_architecture.svg)

---

## Event-Driven Architecture

Event sourcing implementation:

```typescript
// AI implements event-driven system:

interface Event {
  id: string;
  type: string;
  aggregateId: string;
  timestamp: Date;
  data: any;
  metadata: {
    userId?: string;
    correlationId?: string;
  };
}

class EventStore {
  async append(event: Event): Promise<void> {
    // Store event
    await this.db.events.insert(event);

    // Publish to event bus
    await this.eventBus.publish(event.type, event);

    // Update read model
    await this.projectionManager.handle(event);
  }

  async getEvents(aggregateId: string): Promise<Event[]> {
    return this.db.events
      .find({ aggregateId })
      .sort({ timestamp: 1 });
  }

  async replay(aggregateId: string): Promise<any> {
    const events = await this.getEvents(aggregateId);
    return events.reduce((state, event) =>
      this.eventHandlers[event.type](state, event), {});
  }
}

// Event handlers
const eventHandlers = {
  OrderCreated: (state, event) => ({
    ...state,
    id: event.data.orderId,
    items: event.data.items,
    status: 'created'
  }),

  OrderPaid: (state, event) => ({
    ...state,
    status: 'paid',
    paidAt: event.timestamp
  })
};
```

---

## Serverless Development

Lambda function patterns:

```python
# AI creates serverless functions:

import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    """
    AWS Lambda function for processing orders
    """
    try:
        # Parse input
        body = json.loads(event.get('body', '{}'))

        # Validate input
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
            UpdateExpression='SET #status = :status, processedAt = :timestamp',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'processed',
                ':timestamp': datetime.now().isoformat()
            },
            ReturnValues='ALL_NEW'
        )

        # Send to SQS for further processing
        sqs = boto3.client('sqs')
        sqs.send_message(
            QueueUrl=os.environ['QUEUE_URL'],
            MessageBody=json.dumps(response['Attributes'])
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

## Load Testing

Performance testing strategies:

```javascript
// AI generates load testing scripts:

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 200 }, // Ramp up
    { duration: '5m', target: 200 }, // Stay at 200 users
    { duration: '2m', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests under 500ms
    errors: ['rate<0.01'],            // Error rate under 1%
  },
};

export default function () {
  // Test scenarios
  const responses = http.batch([
    ['GET', 'http://api.example.com/users'],
    ['GET', 'http://api.example.com/products'],
    ['POST', 'http://api.example.com/orders',
      JSON.stringify({ productId: 1, quantity: 2 }),
      { headers: { 'Content-Type': 'application/json' } }
    ],
  ]);

  responses.forEach(response => {
    check(response, {
      'status is 200': (r) => r.status === 200,
      'response time < 500ms': (r) => r.timings.duration < 500,
    }) || errorRate.add(1);
  });

  sleep(1);
}
```

---

## Optimization Patterns

Performance optimization techniques:

![optimization_patterns](svg/courses/ai/developing-using-ai/07_tasks/optimization_patterns.svg)

---

## Architecture at Scale

Scaling strategies for growth:

```yaml
# AI designs scalable architecture:

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
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
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
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

---

## Chapter Summary

**Key Takeaways**:

AI accelerates specialized development across all domains

Completed coverage of:
    - Backend development patterns and architecture
    - DevOps automation and infrastructure
    - Mobile cross-platform and native features
    - Testing, security, and optimization
    - Microservices and serverless patterns
    - Scaling strategies for production

Each specialization leverages AI's deep domain knowledge

---

## Next Steps

Coming up in following chapters:

1. **Chapter 7**: Quality and Best Practices - maintaining high standards
1. **Chapter 8**: Real-World Project Workflows - end-to-end development
1. **Chapter 9**: Team Collaboration with AI - enhancing team productivity
1. **Chapter 10**: Advanced AI Usage Patterns - complex workflows

Ready to ensure quality in AI-assisted development!
