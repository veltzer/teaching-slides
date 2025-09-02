# Prompt Engineering for Developers

---

## The Art and Science of AI Communication

Master the language that makes AI understand exactly what you need

This chapter covers:
1. Fundamentals of effective prompting
1. Code generation prompts
1. Debugging and problem-solving prompts
1. Code improvement prompts
1. Advanced prompting techniques

---

## Why Prompt Engineering Matters

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="100" width="250" height="200" fill="#E74C3C" rx="10"/>
  <text x="225" y="150" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Poor Prompt</text>
  <text x="225" y="180" text-anchor="middle" fill="white" font-size="12">"Write code"</text>
  <text x="225" y="210" text-anchor="middle" fill="white" font-size="12">❌ Vague results</text>
  <text x="225" y="230" text-anchor="middle" fill="white" font-size="12">❌ Multiple iterations</text>
  <text x="225" y="250" text-anchor="middle" fill="white" font-size="12">❌ Wasted time</text>
  <rect x="450" y="100" width="250" height="200" fill="#27AE60" rx="10"/>
  <text x="575" y="150" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Great Prompt</text>
  <text x="575" y="180" text-anchor="middle" fill="white" font-size="12">"Specific + Context"</text>
  <text x="575" y="210" text-anchor="middle" fill="white" font-size="12">✓ Precise output</text>
  <text x="575" y="230" text-anchor="middle" fill="white" font-size="12">✓ First try success</text>
  <text x="575" y="250" text-anchor="middle" fill="white" font-size="12">✓ Time saved</text>
  <path d="M 350 200 L 450 200" stroke="#3498DB" stroke-width="3" marker-end="url(#arrow)"/>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#3498DB"/>
    </marker>
  </defs>
</svg>

---

## The Prompt Engineering Formula

Effective prompts contain:

```markdown
CONTEXT + TASK + CONSTRAINTS + FORMAT + EXAMPLES = PERFECT OUTPUT
```

**Context**: Background information and setup
**Task**: What you want accomplished
**Constraints**: Limitations and requirements
**Format**: How output should be structured
**Examples**: Sample inputs/outputs

---

## Fundamentals: Clear Requirement Specification

**Poor**: "Create a user function"

**Better**: "Create a Python function to validate user registration"

### Best

```markdown
Create a Python function that validates user registration with:
- Email format validation
- Password strength check (8+ chars, 1 uppercase, 1 number)
- Username uniqueness check against database
- Return validation errors as a dictionary
- Use type hints and docstrings
```

---

## Context Provision Strategies

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="200" r="150" fill="#3498DB" opacity="0.2"/>
  <circle cx="400" cy="200" r="100" fill="#2ECC71" opacity="0.3"/>
  <circle cx="400" cy="200" r="50" fill="#E74C3C" opacity="0.4"/>
  <text x="400" y="200" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Task</text>
  <text x="400" y="130" text-anchor="middle" font-size="12">Technical Stack</text>
  <text x="400" y="270" text-anchor="middle" font-size="12">Business Context</text>
  <text x="480" y="200" text-anchor="middle" font-size="11">Requirements</text>
  <text x="320" y="200" text-anchor="middle" font-size="11">Constraints</text>
  <text x="400" y="350" text-anchor="middle" font-size="16" font-weight="bold">Layer Context from Broad to Specific</text>
</svg>

---

## Context Layering Example

```markdown
# Broad Context
I'm building an e-commerce platform using Django and PostgreSQL.

# Medium Context
Working on the order processing module that handles payment integration.

# Specific Context
Need to implement webhook handler for Stripe payment confirmations.

# Task
Create a Django view that:
- Verifies Stripe webhook signatures
- Updates order status in database
- Sends confirmation email
- Handles errors gracefully
```

---

## Output Format Control

Specify exactly how you want the output:

```markdown
Provide the solution in this format:

1. Brief explanation (2-3 sentences)
2. Code implementation with comments
3. Example usage
4. Unit test
5. Potential edge cases to consider

Use Python 3.10+ syntax with type hints.
```

---

## Constraint Definition

Be explicit about limitations:

```markdown
Constraints:
- Must complete in under 100ms
- Cannot use external libraries except requests
- Must be Python 3.8 compatible
- Maximum 50 lines of code
- Must handle network failures gracefully
- Follow PEP 8 style guide
```

---

## Iterative Refinement Process

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="150" width="120" height="60" fill="#3498DB" rx="5"/>
  <text x="160" y="185" text-anchor="middle" fill="white" font-size="12">Initial Prompt</text>
  <path d="M 220 180 L 280 180" stroke="#34495E" stroke-width="2" marker-end="url(#arr1)"/>
  <rect x="280" y="150" width="120" height="60" fill="#2ECC71" rx="5"/>
  <text x="340" y="185" text-anchor="middle" fill="white" font-size="12">AI Response</text>
  <path d="M 400 180 L 460 180" stroke="#34495E" stroke-width="2" marker-end="url(#arr2)"/>
  <rect x="460" y="150" width="120" height="60" fill="#E74C3C" rx="5"/>
  <text x="520" y="185" text-anchor="middle" fill="white" font-size="12">Evaluate</text>
  <path d="M 580 180 L 640 180" stroke="#34495E" stroke-width="2" marker-end="url(#arr3)"/>
  <rect x="640" y="150" width="120" height="60" fill="#F39C12" rx="5"/>
  <text x="700" y="185" text-anchor="middle" fill="white" font-size="12">Refine Prompt</text>
  <path d="M 700 210 Q 700 280, 400 280 Q 160 280, 160 210" stroke="#9B59B6" stroke-width="2" fill="none" marker-end="url(#arr4)"/>
  <text x="400" y="320" text-anchor="middle" font-size="14">Iterate until optimal</text>
  <defs>
    <marker id="arr1" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#34495E"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#34495E"/>
    </marker>
    <marker id="arr3" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#34495E"/>
    </marker>
    <marker id="arr4" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#9B59B6"/>
    </marker>
  </defs>
</svg>

---

## Code Generation: Function Specifications

Template for function generation:

```markdown
Create a [language] function with these specifications:

Function name: processUserData
Purpose: [Clear description of what it does]
Parameters:
- userData: object containing user information
- options: configuration object (optional)

Returns: Processed user object with calculated fields

Requirements:
- Input validation
- Error handling for missing fields
- Logging for debugging
- Performance: O(n) complexity

Include JSDoc/docstring documentation.
```

---

## Class Design Prompts

Effective class generation:

```python
"""
Design a Python class for a rate limiter with:

Class name: RateLimiter
Purpose: Limit API calls per user

Properties:
- max_requests: int (requests per window)
- window_size: int (seconds)
- storage: Redis connection

Methods:
- check_limit(user_id): bool - returns if request allowed
- reset(user_id): void - reset user's counter
- get_remaining(user_id): int - remaining requests

Use Redis for distributed state
Include error handling and logging
Follow SOLID principles
"""
```

---

## Algorithm Implementation Prompts

Getting optimal algorithms:

```markdown
Implement the [algorithm name] algorithm in [language]:

Input: [Describe input format and constraints]
Output: [Expected output format]

Requirements:
- Time complexity: O(n log n) or better
- Space complexity: O(n) maximum
- Handle edge cases: empty input, single element, duplicates
- Include comments explaining key steps

Example:
Input: [1, 3, 2, 4, 1]
Output: [1, 1, 2, 3, 4]

Optimize for [speed/memory/readability].
```

---

## Data Structure Creation

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="600" height="300" fill="#2C3E50" rx="10"/>
  <text x="400" y="90" text-anchor="middle" fill="white" font-size="18" font-weight="bold">Data Structure Prompt Template</text>
  <rect x="150" y="120" width="500" height="40" fill="#3498DB" rx="5"/>
  <text x="160" y="145" fill="white" font-size="14">1. Structure Type: Tree, Graph, List, etc.</text>
  <rect x="150" y="170" width="500" height="40" fill="#2ECC71" rx="5"/>
  <text x="160" y="195" fill="white" font-size="14">2. Operations: Insert, Delete, Search, Traverse</text>
  <rect x="150" y="220" width="500" height="40" fill="#E74C3C" rx="5"/>
  <text x="160" y="245" fill="white" font-size="14">3. Complexity Requirements: Time and Space</text>
  <rect x="150" y="270" width="500" height="40" fill="#F39C12" rx="5"/>
  <text x="160" y="295" fill="white" font-size="14">4. Special Properties: Thread-safe, Persistent, etc.</text>
</svg>

---

## API Endpoint Design

Comprehensive API prompts:

```markdown
Design a REST API endpoint for user authentication:

Method: POST
Path: /api/v1/auth/login
Purpose: Authenticate user and return JWT token

Request Body:
{
  "email": "string",
  "password": "string",
  "remember_me": "boolean (optional)"
}

Response:
- 200: Success with token and user data
- 401: Invalid credentials
- 429: Too many attempts
- 500: Server error

Include:
- Input validation
- Rate limiting logic
- Secure password checking
- JWT generation
- Error response format
```

---

## Database Schema Generation

Structured database prompts:

```sql
Design a PostgreSQL schema for a blog system:

Requirements:
- Users can have multiple blogs
- Blogs have posts and categories
- Posts can have tags and comments
- Support for draft/published states
- Audit fields (created_at, updated_at)
- Soft delete capability

Include:
- Table definitions with constraints
- Indexes for common queries
- Foreign key relationships
- Sample data insertion
- Common query examples

Consider performance for 1M+ posts.
```

---

## Debugging Prompts: Error Analysis

Effective debugging requests:

```markdown
Debug this error:

Error message: [paste full error]
Code causing error: [paste relevant code]
Context: [what you were trying to do]
Environment: Python 3.9, Django 4.2, PostgreSQL 14

What I've tried:
1. [First attempt]
2. [Second attempt]

Expected behavior: [what should happen]
Actual behavior: [what's happening]

Please explain:
1. Root cause of the error
2. Step-by-step fix
3. How to prevent in future
```

---

## Bug Reproduction Assistance

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="100" width="150" height="60" fill="#E74C3C" rx="5"/>
  <text x="175" y="135" text-anchor="middle" fill="white" font-size="14">Bug Report</text>
  <path d="M 250 130 L 320 130" stroke="#34495E" stroke-width="2" marker-end="url(#bug1)"/>
  <rect x="320" y="100" width="150" height="60" fill="#F39C12" rx="5"/>
  <text x="395" y="135" text-anchor="middle" fill="white" font-size="14">Reproduce</text>
  <path d="M 470 130 L 540 130" stroke="#34495E" stroke-width="2" marker-end="url(#bug2)"/>
  <rect x="540" y="100" width="150" height="60" fill="#3498DB" rx="5"/>
  <text x="615" y="135" text-anchor="middle" fill="white" font-size="14">Isolate</text>
  <rect x="320" y="200" width="150" height="60" fill="#2ECC71" rx="5"/>
  <text x="395" y="235" text-anchor="middle" fill="white" font-size="14">Fix</text>
  <path d="M 615 160 L 395 200" stroke="#34495E" stroke-width="2" marker-end="url(#bug3)"/>
  <text x="400" y="320" text-anchor="middle" font-size="14">AI assists at each step</text>
  <defs>
    <marker id="bug1" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#34495E"/>
    </marker>
    <marker id="bug2" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#34495E"/>
    </marker>
    <marker id="bug3" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#34495E"/>
    </marker>
  </defs>
</svg>

---

## Fix Suggestion Strategies

Getting actionable solutions:

```markdown
This code is failing intermittently:

[paste problematic code]

Symptoms:
- Works 90% of the time
- Fails under high load
- Error: "Connection pool exhausted"

Environment: Node.js, PostgreSQL, 100 concurrent users

Provide:
1. Most likely cause
2. Quick fix for production
3. Long-term solution
4. Monitoring recommendations
5. Test to verify fix
```

---

## Root Cause Analysis Prompts

Deep problem investigation:

```markdown
Help me find the root cause of this performance issue:

Symptom: API response time increased from 200ms to 2s
When started: After last deployment (commit: abc123)
Affected endpoints: All user-related endpoints

Metrics:
- Database queries: Normal (50ms)
- CPU usage: 80% (was 30%)
- Memory: 4GB/8GB
- Network: Normal

Changed in deployment:
[list changes]

Guide me through systematic debugging.
```

---

## Performance Bottleneck Identification

```markdown
Analyze this code for performance bottlenecks:

[paste code]

Context:
- Processes 10,000 records per minute
- Currently takes 5 seconds per batch
- Target: 1 second per batch

Focus on:
1. Database query optimization
2. Memory usage patterns
3. CPU-intensive operations
4. I/O blocking issues
5. Concurrency opportunities

Provide specific optimization suggestions with expected improvements.
```

---

## Code Improvement: Refactoring Requests

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="250" height="80" fill="#E74C3C" rx="10"/>
  <text x="225" y="95" text-anchor="middle" fill="white" font-size="16">Legacy Code</text>
  <rect x="450" y="50" width="250" height="80" fill="#27AE60" rx="10"/>
  <text x="575" y="95" text-anchor="middle" fill="white" font-size="16">Clean Code</text>
  <path d="M 350 90 L 450 90" stroke="#3498DB" stroke-width="3" marker-end="url(#refactor)"/>
  <text x="400" y="80" text-anchor="middle" font-size="12">Refactor</text>
  <rect x="150" y="160" width="500" height="180" fill="#34495E" rx="5"/>
  <text x="400" y="190" text-anchor="middle" fill="white" font-size="14">Refactoring Goals:</text>
  <text x="180" y="220" fill="white" font-size="12">• Extract methods for clarity</text>
  <text x="180" y="245" fill="white" font-size="12">• Remove code duplication</text>
  <text x="180" y="270" fill="white" font-size="12">• Apply design patterns</text>
  <text x="180" y="295" fill="white" font-size="12">• Improve naming conventions</text>
  <text x="180" y="320" fill="white" font-size="12">• Add error handling</text>
  <defs>
    <marker id="refactor" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#3498DB"/>
    </marker>
  </defs>
</svg>

---

## Optimization Strategy Prompts

```markdown
Optimize this function for [speed/memory/readability]:

[paste current implementation]

Current metrics:
- Execution time: 500ms
- Memory usage: 100MB
- Complexity: O(n²)

Target metrics:
- Execution time: <100ms
- Memory usage: <50MB
- Complexity: O(n log n) or better

Constraints:
- Must maintain backward compatibility
- Cannot use additional libraries
- Must remain readable

Provide optimized version with explanation of changes.
```

---

## Security Enhancement Prompts

```markdown
Review and enhance security for this authentication code:

[paste code]

Check for:
1. SQL injection vulnerabilities
2. XSS attack vectors
3. CSRF protection
4. Password security
5. Session management
6. Rate limiting
7. Input validation
8. Error message information leakage

Provide:
- Identified vulnerabilities with severity
- Fixed code with explanations
- Security best practices checklist
```

---

## Readability Improvements

Making code more maintainable:

```markdown
Improve the readability of this code:

[paste complex code]

Focus on:
- Variable and function naming
- Code organization and structure
- Comment clarity and placement
- Reducing cognitive complexity
- Following language idioms

Maintain functionality while making it easier to understand.
Include brief explanations for major changes.
```

---

## Modern Syntax Updates

```markdown
Modernize this JavaScript code to ES6+:

[paste old JavaScript code]

Update to use:
- Arrow functions where appropriate
- Destructuring
- Template literals
- Async/await instead of callbacks
- Const/let instead of var
- Spread operators
- Optional chaining
- Modern array methods

Explain each modernization and its benefits.
```

---

## Anti-Pattern Removal

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="600" height="300" fill="#2C3E50" rx="10"/>
  <text x="400" y="90" text-anchor="middle" fill="white" font-size="18" font-weight="bold">Common Anti-Patterns to Fix</text>
  <rect x="150" y="120" width="220" height="50" fill="#E74C3C" rx="5"/>
  <text x="260" y="150" text-anchor="middle" fill="white" font-size="14">God Object</text>
  <rect x="430" y="120" width="220" height="50" fill="#E74C3C" rx="5"/>
  <text x="540" y="150" text-anchor="middle" fill="white" font-size="14">Spaghetti Code</text>
  <rect x="150" y="180" width="220" height="50" fill="#F39C12" rx="5"/>
  <text x="260" y="210" text-anchor="middle" fill="white" font-size="14">Copy-Paste Programming</text>
  <rect x="430" y="180" width="220" height="50" fill="#F39C12" rx="5"/>
  <text x="540" y="210" text-anchor="middle" fill="white" font-size="14">Magic Numbers</text>
  <rect x="150" y="240" width="220" height="50" fill="#3498DB" rx="5"/>
  <text x="260" y="270" text-anchor="middle" fill="white" font-size="14">Premature Optimization</text>
  <rect x="430" y="240" width="220" height="50" fill="#3498DB" rx="5"/>
  <text x="540" y="270" text-anchor="middle" fill="white" font-size="14">Callback Hell</text>
</svg>

---

## Advanced Technique: Chain-of-Thought

Breaking down complex problems:

```markdown
Solve this step by step:

Problem: Design a distributed task queue system

Think through:
1. First, identify the core requirements
2. Then, consider the architecture components
3. Next, evaluate message broker options
4. After that, design the worker pool strategy
5. Then, plan failure handling mechanisms
6. Finally, describe the monitoring approach

Show your reasoning at each step before providing the solution.
```

---

## Few-Shot Examples

Learning from examples:

```markdown
Convert these SQL queries to MongoDB queries:

Example 1:
SQL: SELECT * FROM users WHERE age > 25
MongoDB: db.users.find({ age: { $gt: 25 } })

Example 2:
SQL: SELECT name, email FROM users WHERE status = 'active'
MongoDB: db.users.find({ status: 'active' }, { name: 1, email: 1 })

Now convert:
SELECT * FROM orders
WHERE total > 100 AND status IN ('pending', 'processing')
ORDER BY created_at DESC
LIMIT 10
```

---

## Role-Based Prompting

Leveraging expertise:

```markdown
Act as a senior DevOps engineer with 10 years of experience.

Review this Kubernetes deployment configuration:
[paste YAML config]

Evaluate for:
- Security best practices
- Resource optimization
- High availability
- Scalability concerns
- Monitoring setup

Provide recommendations as you would in a production review.
```

---

## Step-by-Step Instructions

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="100" width="100" height="50" fill="#3498DB" rx="5"/>
  <text x="100" y="130" text-anchor="middle" fill="white" font-size="12">Step 1</text>
  <path d="M 150 125 L 200 125" stroke="#34495E" stroke-width="2" marker-end="url(#step1)"/>
  <rect x="200" y="100" width="100" height="50" fill="#2ECC71" rx="5"/>
  <text x="250" y="130" text-anchor="middle" fill="white" font-size="12">Step 2</text>
  <path d="M 300 125 L 350 125" stroke="#34495E" stroke-width="2" marker-end="url(#step2)"/>
  <rect x="350" y="100" width="100" height="50" fill="#E74C3C" rx="5"/>
  <text x="400" y="130" text-anchor="middle" fill="white" font-size="12">Step 3</text>
  <path d="M 450 125 L 500 125" stroke="#34495E" stroke-width="2" marker-end="url(#step3)"/>
  <rect x="500" y="100" width="100" height="50" fill="#F39C12" rx="5"/>
  <text x="550" y="130" text-anchor="middle" fill="white" font-size="12">Step 4</text>
  <path d="M 600 125 L 650 125" stroke="#34495E" stroke-width="2" marker-end="url(#step4)"/>
  <rect x="650" y="100" width="100" height="50" fill="#9B59B6" rx="5"/>
  <text x="700" y="130" text-anchor="middle" fill="white" font-size="12">Result</text>
  <text x="100" y="180" font-size="12">Parse Input</text>
  <text x="250" y="180" font-size="12">Validate</text>
  <text x="400" y="180" font-size="12">Process</text>
  <text x="550" y="180" font-size="12">Format</text>
  <text x="700" y="180" font-size="12">Output</text>
  <text x="400" y="250" text-anchor="middle" font-size="16" font-weight="bold">Break Complex Tasks into Steps</text>
  <defs>
    <marker id="step1" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#34495E"/>
    </marker>
    <marker id="step2" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#34495E"/>
    </marker>
    <marker id="step3" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#34495E"/>
    </marker>
    <marker id="step4" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#34495E"/>
    </marker>
  </defs>
</svg>

---

## Negative Examples

Learning from what NOT to do:

```markdown
Create a password validation function.

AVOID these common mistakes:
- Don't store passwords in plain text
- Don't use weak regex like .{8,}
- Don't leak validation details in errors
- Don't allow common passwords
- Don't ignore Unicode characters

Instead, implement proper validation with:
- Minimum complexity requirements
- Secure error messages
- Common password checking
- Proper character handling
```

---

## Output Structuring

Controlling response format:

```markdown
Analyze this code and provide results in this exact format:

## Summary
[One paragraph overview]

## Issues Found
1. **Critical**: [issue and impact]
2. **High**: [issue and impact]
3. **Medium**: [issue and impact]

## Recommendations
- [ ] [Specific action item]
- [ ] [Specific action item]

## Code Fixes

```language
[Fixed code here]

## Estimated Impact
Time saved: [estimate]
Performance gain: [estimate]
```

---

## Prompt Templates Library

Building reusable templates:

```markdown
# Bug Fix Template
I encountered this error: {error_message}
In this code: {code_snippet}
While trying to: {user_action}
Environment: {tech_stack}
Fix the issue and explain the cause.

# Performance Optimization Template
Optimize this {code_type} for {metric}:
{code}
Current performance: {current_metric}
Target: {target_metric}
Constraints: {limitations}

# Code Review Template
Review this {language} code for {project_type}:
{code}
Focus on: {priorities}
Team standards: {guidelines}
```
