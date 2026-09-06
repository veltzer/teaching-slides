---
tags:
  - data-and-ai:ai
  - data-and-ai:generative-ai
  - languages:python
  - data-and-ai:prompt-engineering
  - concepts:ethics
level: intermediate
category: ai
audience:
  - audiences:data-scientists

---

# Making a Customized Database Interface

---

## The Vision: Natural Language to SQL

![the_vision_natural_language_to_sql](svg/courses/ai/generative-ai-applications/12_custom_database_interface/the_vision_natural_language_to_sql.svg)

---

## Architecture Overview

![architecture_overview](svg/courses/ai/generative-ai-applications/12_custom_database_interface/architecture_overview.svg)

---

## NL to SQL Pipeline

![nl_to_sql_architecture](svg/courses/ai/generative-ai-applications/12_custom_database_interface/nl_to_sql_architecture.svg)

---

## Setting Up the Database

```python
import sqlite3

def create_sample_database():
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            industry TEXT,
            created_at DATE
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price DECIMAL(10,2)
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(id),
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER,
            total DECIMAL(10,2),
            order_date DATE
        );
```

---

## Setting Up the Database: Sample Data

```python
        -- Insert sample data
        INSERT INTO customers VALUES
            (1, 'Acme Corp', 'info@acme.com', 'Manufacturing', '2023-01-15'),
            (2, 'TechStart', 'hello@techstart.io', 'Technology', '2023-03-22'),
            (3, 'GreenEnergy', 'contact@green.com', 'Energy', '2023-06-10');
    """)
    conn.commit()
    return conn
```

---

## Extracting Schema Information

```python
def get_schema_info(conn):
    """Extract database schema for LLM context."""
    cursor = conn.cursor()

    # Get all tables
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    tables = [row[0] for row in cursor.fetchall()]

    schema_info = []
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()

        col_descriptions = []
        for col in columns:
            col_id, name, dtype, notnull, default, pk = col
            col_descriptions.append(
                f"  - {name} ({dtype})"
                f"{'  PRIMARY KEY' if pk else ''}"
                f"{'  NOT NULL' if notnull else ''}"
            )

        # Get sample data
        cursor.execute(f"SELECT * FROM {table} LIMIT 3")
        samples = cursor.fetchall()

        schema_info.append(
            f"Table: {table}\n"
            f"Columns:\n" + "\n".join(col_descriptions) +
            f"\nSample rows: {samples}\n"
        )

    return "\n".join(schema_info)
```

---

## The Query Generator

```python
from openai import OpenAI

client = OpenAI()

def generate_sql(user_question, schema, conn):
    """Convert natural language question to SQL."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""You are a SQL expert.
Given the database schema below, generate a SQLite query to answer
the user's question.

SCHEMA:
{schema}

RULES:
- Return ONLY the SQL query, no explanation
- Use SQLite syntax
- Never use DELETE, UPDATE, INSERT, DROP, or ALTER
- Always use table aliases for clarity
- Include ORDER BY when relevant
- Limit results to 20 rows unless specified"""},
            {"role": "user", "content": user_question},
        ],
        temperature=0,
    )

    sql = response.choices[0].message.content.strip()
    # Clean up markdown code blocks if present
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql
```

---

## SQL Validation and Safety

```python
import re

class SQLValidator:
    """Validate generated SQL before execution."""

    FORBIDDEN_KEYWORDS = [
        "DROP", "DELETE", "INSERT", "UPDATE", "ALTER",
        "CREATE", "TRUNCATE", "EXEC", "EXECUTE",
        "GRANT", "REVOKE", "--", "/*",
    ]

    def validate(self, sql):
        """Check SQL for safety and correctness."""
        errors = []

        # Check for forbidden operations
        sql_upper = sql.upper()
        for keyword in self.FORBIDDEN_KEYWORDS:
            if keyword in sql_upper:
                errors.append(f"Forbidden keyword: {keyword}")

        # Check for multiple statements
        if sql.count(";") > 1:
            errors.append("Multiple statements not allowed")

        # Must be a SELECT query
        if not sql_upper.strip().startswith("SELECT"):
            errors.append("Only SELECT queries are allowed")

        if errors:
            raise ValueError(f"SQL validation failed: {errors}")

        return True

validator = SQLValidator()
```

---

## Executing Queries and Formatting Results

```python
def execute_and_format(sql, conn, user_question):
    """Execute SQL and format results as natural language."""
    # Validate first
    validator.validate(sql)

    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    if not rows:
        return "No results found for your query."

    # Format as table for LLM
    result_text = f"Columns: {columns}\n"
    for row in rows[:20]:
        result_text += f"  {dict(zip(columns, row))}\n"

    # Generate natural language response
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content":
                "Convert database query results into a clear, "
                "natural language response. Include key numbers "
                "and insights. Format nicely with bullet points."},
            {"role": "user", "content":
                f"Question: {user_question}\n"
                f"SQL: {sql}\n"
                f"Results:\n{result_text}"},
        ],
    )
    return response.choices[0].message.content
```

---

## Putting It All Together

```python
class DatabaseAssistant:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.schema = get_schema_info(self.conn)
        self.validator = SQLValidator()
        self.history = []

    def query(self, question):
        """Full pipeline: question → SQL → execute → response."""
        try:
            # Generate SQL
            sql = generate_sql(question, self.schema, self.conn)
            print(f"Generated SQL: {sql}")

            # Validate
            self.validator.validate(sql)

            # Execute and format
            response = execute_and_format(
                sql, self.conn, question
            )

            # Store in history
            self.history.append({
                "question": question,
                "sql": sql,
                "response": response,
            })

            return response

        except Exception as e:
            return f"Error processing query: {e}"

# Usage
db = DatabaseAssistant("company.db")
print(db.query("Which industry has the most customers?"))
print(db.query("What's the average order value by product?"))
```

---

## Using LangChain SQL Agent

```python
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

# Connect to database
db = SQLDatabase.from_uri("sqlite:///company.db")

# See what LangChain detects
print(db.get_table_info())

# Create SQL agent
llm = ChatOpenAI(model="gpt-4o", temperature=0)

agent = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="tool-calling",
    verbose=True,  # See the reasoning process
)

# Use the agent
result = agent.invoke({
    "input": "Which customer has placed the most orders? "
             "Show their name and total number of orders."
})
print(result["output"])

# The agent will:
# 1. Examine the schema
# 2. Write and test SQL
# 3. Handle errors and retry
# 4. Format the final answer
```

---

## Error Recovery and Self-Correction

```python
def query_with_retry(question, schema, conn, max_retries=3):
    """Generate and execute SQL with error recovery."""

    sql = generate_sql(question, schema, conn)
    errors_so_far = []

    for attempt in range(max_retries):
        try:
            validator.validate(sql)
            result = execute_query(sql, conn)
            return format_result(result, question)

        except Exception as e:
            errors_so_far.append(f"Attempt {attempt+1}: {str(e)}")

            # Ask LLM to fix the SQL
            fix_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content":
                        f"Fix this SQL query. Schema:\n{schema}"},
                    {"role": "user", "content":
                        f"Original question: {question}\n"
                        f"Failed SQL: {sql}\n"
                        f"Error: {e}\n"
                        f"Provide only the corrected SQL."},
                ],
                temperature=0,
            )
            sql = fix_response.choices[0].message.content.strip()
            sql = sql.replace("```sql", "").replace("```", "").strip()

    return f"Failed after {max_retries} attempts: {errors_so_far}"
```

---

## Adding Conversation Context

```python
class ConversationalDBAssistant(DatabaseAssistant):
    """Database assistant with conversation memory."""

    def query(self, question):
        # Include conversation history for context
        history_context = ""
        if self.history:
            recent = self.history[-3:]  # Last 3 interactions
            for h in recent:
                history_context += (
                    f"Previous Q: {h['question']}\n"
                    f"Previous SQL: {h['sql']}\n\n"
                )

        # Modified prompt includes history
        sql = generate_sql_with_context(
            question, self.schema, history_context
        )
        # ... rest of pipeline

# This enables follow-up questions:
# User: "Show me all customers in Technology"
# User: "Now show their total orders"  ← "their" = Technology customers
# User: "Sort those by date"  ← "those" = previous results
```

---

## Visualization Integration

```python
import matplotlib.pyplot as plt
import io
import base64

def auto_visualize(sql_result, question):
    """Auto-generate chart from query results."""
    columns, rows = sql_result

    # Ask LLM what chart type to use
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content":
                "Given a data query, suggest the best chart type. "
                "Respond with only: bar, line, pie, or table."},
            {"role": "user", "content":
                f"Question: {question}\n"
                f"Columns: {columns}\n"
                f"Row count: {len(rows)}"},
        ],
    )
    chart_type = response.choices[0].message.content.strip()

    if chart_type == "bar" and len(columns) >= 2:
        labels = [row[0] for row in rows]
        values = [row[1] for row in rows]
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values)
        plt.title(question)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("chart.png")
        return "chart.png"
```

---

## Security Best Practices

![security_best_practices](svg/courses/ai/generative-ai-applications/12_custom_database_interface/security_best_practices.svg)

---

## Exercise: Build Your Database Assistant

```python
"""
Exercise: Build a complete database interface.

1. Create a SQLite database with at least 3 related tables:
   - employees (id, name, department, salary, hire_date)
   - departments (id, name, budget, manager_id)
   - projects (id, name, department_id, status, deadline)

2. Populate with 20+ rows of realistic data

3. Build the full pipeline:
   - Schema extraction
   - NL → SQL generation
   - SQL validation
   - Query execution
   - Result formatting

4. Test with these queries:
   - "Which department has the highest average salary?"
   - "List all overdue projects"
   - "Who are the newest employees?"
   - "Show department budgets vs total salaries"

5. Add error handling and retry logic

Bonus:
- Add conversation memory for follow-up questions
- Auto-generate charts for numeric results
"""
```

---

## Day 3 Summary and Q&A

**What we covered today:**
- AI agents: architecture, planning, and the observe-think-act loop
- Memory systems: buffer, summary, vector, and entity memory
- RAG: retrieval-augmented generation for knowledge-grounded responses
- `LangChain`: chains, prompts, document loaders, vector stores, agents
- Custom database interfaces: NL-to-SQL with validation and formatting

**Key insight:** The combination of `LLM` reasoning + external tools + persistent memory unlocks a new class of intelligent applications.

**Tomorrow:** We move to open-source models with `HuggingFace` and efficient fine-tuning techniques.

---

## Handling Ambiguous Queries

```python
def handle_ambiguous_query(question, schema):
    """Detect and resolve ambiguous user questions."""

    clarification_check = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content":
                f"Given this database schema:\n{schema}\n\n"
                f"Determine if the following question is "
                f"ambiguous or needs clarification. "
                f"If clear, respond 'CLEAR'. "
                f"If ambiguous, respond with a clarifying question."},
            {"role": "user", "content": question},
        ],
    )

    response = clarification_check.choices[0].message.content

    if "CLEAR" not in response:
        return {"needs_clarification": True, "question": response}

    return {"needs_clarification": False}

# Examples:
# "Show me the top customers"
# → "By what metric? Revenue, order count, or recency?"
#
# "What's the revenue?"
# → "For what time period? All time, this year, or this quarter?"
```

---

## Natural Language to SQL — Advanced Patterns

```python
# Handling complex queries with subqueries and CTEs

complex_query_prompt = """You are an expert SQL developer.
Generate SQLite queries for complex analytical questions.

Schema: {schema}

Use CTEs for readability. Examples of supported patterns:

1. Window functions:
   SELECT name, salary,
     RANK() OVER (PARTITION BY dept ORDER BY salary DESC)
   FROM employees

2. Common Table Expressions:
   WITH monthly_sales AS (
     SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
     FROM orders GROUP BY 1
   )
   SELECT month, total,
     total - LAG(total) OVER (ORDER BY month) as growth
   FROM monthly_sales

3. Conditional aggregation:
   SELECT dept,
     COUNT(CASE WHEN status='active' THEN 1 END) as active,
     COUNT(CASE WHEN status='inactive' THEN 1 END) as inactive
   FROM employees GROUP BY dept

Question: {question}

Generate ONLY the SQL query."""
```

---

## Performance Optimization

```python
class OptimizedDBAssistant:
    """Database assistant with caching and optimization."""

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.schema = get_schema_info(self.conn)
        self.query_cache = {}
        self.schema_hash = hash(self.schema)

    def query(self, question):
        # Check cache for similar questions
        cache_key = self._normalize_question(question)
        if cache_key in self.query_cache:
            cached_sql = self.query_cache[cache_key]
            return self._execute(cached_sql, question)

        sql = generate_sql(question, self.schema, self.conn)

        # Add LIMIT if not present (safety)
        if "LIMIT" not in sql.upper():
            sql = sql.rstrip(";") + " LIMIT 100;"

        # Add query timeout
        self.conn.execute("PRAGMA busy_timeout = 5000")

        # Cache the successful query
        self.query_cache[cache_key] = sql

        return self._execute(sql, question)

    def _normalize_question(self, question):
        """Normalize question for cache lookup."""
        return " ".join(question.lower().split())
```

---

## Multi-Database Support

```python
class MultiDBAssistant:
    """Query across multiple databases."""

    def __init__(self, databases):
        self.databases = {}
        for name, config in databases.items():
            self.databases[name] = {
                "conn": sqlite3.connect(config["path"]),
                "schema": get_schema_info(
                    sqlite3.connect(config["path"])
                ),
                "description": config["description"],
            }

    def route_query(self, question):
        """Determine which database to query."""
        db_descriptions = "\n".join(
            f"- {name}: {db['description']}"
            for name, db in self.databases.items()
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content":
                    f"Choose the best database:\n{db_descriptions}"},
                {"role": "user", "content": question},
            ],
        )
        db_name = response.choices[0].message.content.strip()
        return self.databases.get(db_name)

# Usage
assistant = MultiDBAssistant({
    "sales": {"path": "sales.db", "description": "Sales and orders"},
    "hr": {"path": "hr.db", "description": "Employees and departments"},
    "support": {"path": "support.db", "description": "Customer tickets"},
})
```

---

## Query Explanation — Teaching Users SQL

```python
def explain_query(sql, question):
    """Generate a human-readable explanation of the SQL."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content":
                "Explain this SQL query in plain English. "
                "Break down each clause. Use simple language."},
            {"role": "user", "content":
                f"User asked: {question}\n\n"
                f"Generated SQL:\n{sql}\n\n"
                f"Explain what this query does step by step."},
        ],
    )
    return response.choices[0].message.content

# Example output:
# "This query does the following:
#  1. Looks at the 'orders' table joined with 'customers'
#  2. Filters to only orders from this quarter
#  3. Groups the results by customer name
#  4. Adds up the total amount for each customer
#  5. Sorts by total amount, highest first
#  6. Shows only the top 5 results"
```

---

## Suggested Queries — Proactive Assistance

```python
def suggest_queries(schema, conversation_history=None):
    """Generate suggested questions based on the database."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content":
                f"Based on this database schema:\n{schema}\n\n"
                f"Suggest 5 interesting analytical questions "
                f"a business user might want to ask. "
                f"Make them specific and actionable."},
            {"role": "user", "content":
                "What are good questions to explore this data?"},
        ],
    )
    return response.choices[0].message.content

# Output example:
# 1. "Which product category has the highest growth rate?"
# 2. "Are there any customers at risk of churning?"
# 3. "What day of the week generates the most orders?"
# 4. "Which sales rep has the best conversion rate?"
# 5. "How does average order value change by season?"
```

---

## Testing Your Database Assistant

```python
class DBAssistantTestSuite:
    """Automated tests for the database assistant."""

    def __init__(self, assistant):
        self.assistant = assistant
        self.test_cases = [
            {
                "question": "How many customers do we have?",
                "expected_sql_contains": ["COUNT", "customers"],
                "expected_type": "number",
            },
            {
                "question": "Who is our top customer by revenue?",
                "expected_sql_contains": ["ORDER BY", "DESC", "LIMIT"],
                "expected_type": "name",
            },
            {
                "question": "Show monthly revenue trend",
                "expected_sql_contains": ["GROUP BY", "strftime"],
                "expected_type": "table",
            },
        ]

    def run_tests(self):
        passed = 0
        for i, test in enumerate(self.test_cases):
            try:
                result = self.assistant.query(test["question"])
                # Verify SQL contains expected clauses
                sql = self.assistant.history[-1]["sql"]
                for expected in test["expected_sql_contains"]:
                    assert expected.upper() in sql.upper(), \
                        f"Missing '{expected}' in SQL"
                passed += 1
                print(f"  Test {i+1}: PASS")
            except Exception as e:
                print(f"  Test {i+1}: FAIL — {e}")
        print(f"\nResults: {passed}/{len(self.test_cases)} passed")
```

---

## Exporting Results

```python
import csv
import json

class ExportableDBAssistant(DatabaseAssistant):
    """Database assistant with export capabilities."""

    def query_to_csv(self, question, output_path):
        """Execute query and export results to CSV."""
        sql = generate_sql(question, self.schema, self.conn)
        self.validator.validate(sql)

        cursor = self.conn.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)

        return f"Exported {len(rows)} rows to {output_path}"

    def query_to_json(self, question):
        """Execute query and return structured JSON."""
        sql = generate_sql(question, self.schema, self.conn)
        self.validator.validate(sql)

        cursor = self.conn.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]
```
