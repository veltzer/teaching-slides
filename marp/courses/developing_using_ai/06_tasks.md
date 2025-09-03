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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="200" r="150" fill="#3498DB" opacity="0.2"/>
  <circle cx="400" cy="200" r="100" fill="#2ECC71" opacity="0.3"/>
  <circle cx="400" cy="200" r="50" fill="#E74C3C" opacity="0.4"/>
  <text x="400" y="200" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Core AI</text>
  <rect x="100" y="50" width="150" height="60" fill="#9B59B6" rx="5"/>
  <text x="175" y="85" text-anchor="middle" fill="white" font-size="14">Database</text>
  <rect x="550" y="50" width="150" height="60" fill="#F39C12" rx="5"/>
  <text x="625" y="85" text-anchor="middle" fill="white" font-size="14">Frontend</text>
  <rect x="100" y="290" width="150" height="60" fill="#1ABC9C" rx="5"/>
  <text x="175" y="325" text-anchor="middle" fill="white" font-size="14">Backend</text>
  <rect x="550" y="290" width="150" height="60" fill="#E67E22" rx="5"/>
  <text x="625" y="325" text-anchor="middle" fill="white" font-size="14">DevOps</text>
  <line x1="250" y1="80" x2="350" y2="150" stroke="#34495E" stroke-width="2"/>
  <line x1="550" y1="80" x2="450" y2="150" stroke="#34495E" stroke-width="2"/>
  <line x1="250" y1="320" x2="350" y2="250" stroke="#34495E" stroke-width="2"/>
  <line x1="550" y1="320" x2="450" y2="250" stroke="#34495E" stroke-width="2"/>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="600" height="300" fill="#2C3E50" rx="10"/>
  <text x="400" y="80" text-anchor="middle" fill="white" font-size="18" font-weight="bold">Query Performance Analysis</text>
  <rect x="150" y="100" width="500" height="40" fill="#E74C3C" rx="5"/>
  <text x="160" y="125" fill="white" font-size="12">Before: SELECT * FROM orders WHERE status = 'pending'</text>
  <text x="550" y="125" fill="white" font-size="12">Time: 2.5s</text>
  <rect x="150" y="150" width="500" height="80" fill="#27AE60" rx="5"/>
  <text x="160" y="175" fill="white" font-size="12">After: WITH pending_orders AS (</text>
  <text x="180" y="195" fill="white" font-size="12">SELECT id, customer_id, total FROM orders</text>
  <text x="180" y="215" fill="white" font-size="12">WHERE status = 'pending' AND created_at > NOW() - INTERVAL '7 days'</text>
  <text x="160" y="235" fill="white" font-size="12">) SELECT * FROM pending_orders;</text>
  <text x="550" y="195" fill="white" font-size="12">Time: 0.08s</text>
  <rect x="150" y="250" width="500" height="60" fill="#3498DB" rx="5"/>
  <text x="160" y="275" fill="white" font-size="12">Optimizations Applied:</text>
  <text x="160" y="295" fill="white" font-size="12">✓ Partial index ✓ Column selection ✓ Date range ✓ CTE usage</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">NoSQL vs SQL Data Models</text>
  <rect x="50" y="50" width="340" height="320" fill="#3498DB" rx="10"/>
  <text x="220" y="80" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Relational (SQL)</text>
  <rect x="70" y="100" width="300" height="60" fill="#2980B9" rx="5"/>
  <text x="220" y="125" text-anchor="middle" fill="white" font-size="12">Users Table</text>
  <text x="220" y="145" text-anchor="middle" fill="white" font-size="10">id | name | email | created_at</text>
  <rect x="70" y="170" width="300" height="60" fill="#2980B9" rx="5"/>
  <text x="220" y="195" text-anchor="middle" fill="white" font-size="12">Orders Table</text>
  <text x="220" y="215" text-anchor="middle" fill="white" font-size="10">id | user_id | total | status</text>
  <line x1="220" y1="160" x2="220" y2="170" stroke="white" stroke-width="2"/>
  <text x="230" y="165" fill="white" font-size="10">FK</text>
  <rect x="410" y="50" width="340" height="320" fill="#27AE60" rx="10"/>
  <text x="580" y="80" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Document (NoSQL)</text>
  <rect x="430" y="100" width="300" height="250" fill="#229954" rx="5"/>
  <text x="580" y="125" text-anchor="middle" fill="white" font-size="12">User Document</text>
  <text x="450" y="150" fill="white" font-size="10">{</text>
  <text x="460" y="170" fill="white" font-size="10">  "_id": "user123",</text>
  <text x="460" y="190" fill="white" font-size="10">  "name": "John Doe",</text>
  <text x="460" y="210" fill="white" font-size="10">  "email": "john@example.com",</text>
  <text x="460" y="230" fill="white" font-size="10">  "orders": [</text>
  <text x="470" y="250" fill="white" font-size="10">    { "id": "ord1", "total": 99.99 },</text>
  <text x="470" y="270" fill="white" font-size="10">    { "id": "ord2", "total": 149.99 }</text>
  <text x="460" y="290" fill="white" font-size="10">  ],</text>
  <text x="460" y="310" fill="white" font-size="10">  "preferences": { ... }</text>
  <text x="450" y="330" fill="white" font-size="10">}</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="600" height="300" fill="#2C3E50" rx="10"/>
  <text x="400" y="80" text-anchor="middle" fill="white" font-size="18" font-weight="bold">CSS Architecture Approaches</text>
  <rect x="150" y="100" width="140" height="80" fill="#3498DB" rx="5"/>
  <text x="220" y="130" text-anchor="middle" fill="white" font-size="14">Utility-First</text>
  <text x="220" y="150" text-anchor="middle" fill="white" font-size="10">Tailwind CSS</text>
  <text x="220" y="165" text-anchor="middle" fill="white" font-size="10">Fast prototyping</text>
  <rect x="310" y="100" width="140" height="80" fill="#9B59B6" rx="5"/>
  <text x="380" y="130" text-anchor="middle" fill="white" font-size="14">CSS-in-JS</text>
  <text x="380" y="150" text-anchor="middle" fill="white" font-size="10">styled-components</text>
  <text x="380" y="165" text-anchor="middle" fill="white" font-size="10">Component scope</text>
  <rect x="470" y="100" width="140" height="80" fill="#E74C3C" rx="5"/>
  <text x="540" y="130" text-anchor="middle" fill="white" font-size="14">CSS Modules</text>
  <text x="540" y="150" text-anchor="middle" fill="white" font-size="10">Local scope</text>
  <text x="540" y="165" text-anchor="middle" fill="white" font-size="10">Build-time</text>
  <rect x="150" y="200" width="140" height="80" fill="#27AE60" rx="5"/>
  <text x="220" y="230" text-anchor="middle" fill="white" font-size="14">BEM</text>
  <text x="220" y="250" text-anchor="middle" fill="white" font-size="10">Methodology</text>
  <text x="220" y="265" text-anchor="middle" fill="white" font-size="10">Naming convention</text>
  <rect x="310" y="200" width="140" height="80" fill="#F39C12" rx="5"/>
  <text x="380" y="230" text-anchor="middle" fill="white" font-size="14">Sass/SCSS</text>
  <text x="380" y="250" text-anchor="middle" fill="white" font-size="10">Preprocessor</text>
  <text x="380" y="265" text-anchor="middle" fill="white" font-size="10">Variables, mixins</text>
  <rect x="470" y="200" width="140" height="80" fill="#1ABC9C" rx="5"/>
  <text x="540" y="230" text-anchor="middle" fill="white" font-size="14">PostCSS</text>
  <text x="540" y="250" text-anchor="middle" fill="white" font-size="10">Transform CSS</text>
  <text x="540" y="265" text-anchor="middle" fill="white" font-size="10">Plugin ecosystem</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="18" font-weight="bold">Animation Performance Hierarchy</text>
  <rect x="100" y="70" width="600" height="60" fill="#27AE60" rx="10"/>
  <text x="400" y="105" text-anchor="middle" fill="white" font-size="14">✅ Transform & Opacity (GPU accelerated)</text>
  <text x="400" y="120" text-anchor="middle" fill="white" font-size="10">Best performance - 60 FPS</text>
  <rect x="100" y="150" width="600" height="60" fill="#F39C12" rx="10"/>
  <text x="400" y="185" text-anchor="middle" fill="white" font-size="14">⚠️ Color & Shadow Changes</text>
  <text x="400" y="200" text-anchor="middle" fill="white" font-size="10">Triggers repaint - Moderate performance</text>
  <rect x="100" y="230" width="600" height="60" fill="#E74C3C" rx="10"/>
  <text x="400" y="265" text-anchor="middle" fill="white" font-size="14">❌ Width, Height, Position Changes</text>
  <text x="400" y="280" text-anchor="middle" fill="white" font-size="10">Triggers reflow - Poor performance</text>
  <rect x="200" y="310" width="400" height="50" fill="#3498DB" rx="5"/>
  <text x="400" y="340" text-anchor="middle" fill="white" font-size="12">Use will-change and transform3d for optimization</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="600" height="300" fill="#2C3E50" rx="10"/>
  <text x="400" y="80" text-anchor="middle" fill="white" font-size="18" font-weight="bold">Infrastructure as Code</text>
  <rect x="150" y="100" width="180" height="60" fill="#FF9900" rx="5"/>
  <text x="240" y="135" text-anchor="middle" fill="white" font-size="14">Terraform</text>
  <rect x="360" y="100" width="180" height="60" fill="#326CE5" rx="5"/>
  <text x="450" y="135" text-anchor="middle" fill="white" font-size="14">Kubernetes</text>
  <rect x="150" y="180" width="180" height="60" fill="#2596BE" rx="5"/>
  <text x="240" y="215" text-anchor="middle" fill="white" font-size="14">Docker</text>
  <rect x="360" y="180" width="180" height="60" fill="#FF6C37" rx="5"/>
  <text x="450" y="215" text-anchor="middle" fill="white" font-size="14">Ansible</text>
  <rect x="150" y="260" width="180" height="60" fill="#40B5A4" rx="5"/>
  <text x="240" y="295" text-anchor="middle" fill="white" font-size="14">CloudFormation</text>
  <rect x="360" y="260" width="180" height="60" fill="#E535AB" rx="5"/>
  <text x="450" y="295" text-anchor="middle" fill="white" font-size="14">Pulumi</text>
  <text x="600" y="200" text-anchor="middle" fill="white" font-size="12">Define</text>
  <text x="600" y="220" text-anchor="middle" fill="white" font-size="12">Version</text>
  <text x="600" y="240" text-anchor="middle" fill="white" font-size="12">Deploy</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="600" height="300" fill="#2C3E50" rx="10"/>
  <text x="400" y="80" text-anchor="middle" fill="white" font-size="18" font-weight="bold">Observability Stack</text>
  <rect x="150" y="110" width="150" height="60" fill="#E6522C" rx="5"/>
  <text x="225" y="145" text-anchor="middle" fill="white" font-size="14">Prometheus</text>
  <text x="225" y="160" text-anchor="middle" fill="white" font-size="10">Metrics</text>
  <rect x="325" y="110" width="150" height="60" fill="#F46800" rx="5"/>
  <text x="400" y="145" text-anchor="middle" fill="white" font-size="14">Grafana</text>
  <text x="400" y="160" text-anchor="middle" fill="white" font-size="10">Visualization</text>
  <rect x="500" y="110" width="150" height="60" fill="#00A8E1" rx="5"/>
  <text x="575" y="145" text-anchor="middle" fill="white" font-size="14">ELK Stack</text>
  <text x="575" y="160" text-anchor="middle" fill="white" font-size="10">Logs</text>
  <rect x="150" y="200" width="150" height="60" fill="#4B3F72" rx="5"/>
  <text x="225" y="235" text-anchor="middle" fill="white" font-size="14">Jaeger</text>
  <text x="225" y="250" text-anchor="middle" fill="white" font-size="10">Tracing</text>
  <rect x="325" y="200" width="150" height="60" fill="#FF6B6B" rx="5"/>
  <text x="400" y="235" text-anchor="middle" fill="white" font-size="14">PagerDuty</text>
  <text x="400" y="250" text-anchor="middle" fill="white" font-size="10">Alerting</text>
  <rect x="500" y="200" width="150" height="60" fill="#7E57C2" rx="5"/>
  <text x="575" y="235" text-anchor="middle" fill="white" font-size="14">DataDog</text>
  <text x="575" y="250" text-anchor="middle" fill="white" font-size="10">APM</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="18" font-weight="bold">Cross-Platform Development Options</text>
  <rect x="50" y="70" width="220" height="280" fill="#61DAFB" rx="10"/>
  <text x="160" y="100" text-anchor="middle" fill="#282C34" font-size="16" font-weight="bold">React Native</text>
  <text x="160" y="130" text-anchor="middle" font-size="12">Performance: ⭐⭐⭐⭐</text>
  <text x="160" y="155" text-anchor="middle" font-size="12">Learning: ⭐⭐⭐</text>
  <text x="160" y="180" text-anchor="middle" font-size="12">• JavaScript/React</text>
  <text x="160" y="205" text-anchor="middle" font-size="12">• Native modules</text>
  <text x="160" y="230" text-anchor="middle" font-size="12">• Hot reload</text>
  <text x="160" y="255" text-anchor="middle" font-size="12">• Large ecosystem</text>
  <rect x="290" y="70" width="220" height="280" fill="#02569B" rx="10"/>
  <text x="400" y="100" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Flutter</text>
  <text x="400" y="130" text-anchor="middle" fill="white" font-size="12">Performance: ⭐⭐⭐⭐⭐</text>
  <text x="400" y="155" text-anchor="middle" fill="white" font-size="12">Learning: ⭐⭐⭐⭐</text>
  <text x="400" y="180" text-anchor="middle" fill="white" font-size="12">• Dart language</text>
  <text x="400" y="205" text-anchor="middle" fill="white" font-size="12">• Custom rendering</text>
  <text x="400" y="230" text-anchor="middle" fill="white" font-size="12">• Rich widgets</text>
  <text x="400" y="255" text-anchor="middle" fill="white" font-size="12">• Fast performance</text>
  <rect x="530" y="70" width="220" height="280" fill="#007ACC" rx="10"/>
  <text x="640" y="100" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Ionic</text>
  <text x="640" y="130" text-anchor="middle" fill="white" font-size="12">Performance: ⭐⭐⭐</text>
  <text x="640" y="155" text-anchor="middle" fill="white" font-size="12">Learning: ⭐⭐</text>
  <text x="640" y="180" text-anchor="middle" fill="white" font-size="12">• Web technologies</text>
  <text x="640" y="205" text-anchor="middle" fill="white" font-size="12">• Angular/React/Vue</text>
  <text x="640" y="230" text-anchor="middle" fill="white" font-size="12">• Capacitor plugins</text>
  <text x="640" y="255" text-anchor="middle" fill="white" font-size="12">• PWA support</text>
</svg>

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
