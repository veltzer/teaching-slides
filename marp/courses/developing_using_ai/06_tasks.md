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
