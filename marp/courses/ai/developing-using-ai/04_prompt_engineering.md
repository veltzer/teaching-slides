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

![why_prompt_engineering_matters](svg/courses/ai/developing-using-ai/04_prompt_engineering/why_prompt_engineering_matters.svg)

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

![context_provision_strategies](svg/courses/ai/developing-using-ai/04_prompt_engineering/context_provision_strategies.svg)

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

![iterative_refinement_process](svg/courses/ai/developing-using-ai/04_prompt_engineering/iterative_refinement_process.svg)

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

![data_structure_creation](svg/courses/ai/developing-using-ai/04_prompt_engineering/data_structure_creation.svg)

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

![bug_reproduction_assistance](svg/courses/ai/developing-using-ai/04_prompt_engineering/bug_reproduction_assistance.svg)

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

![code_improvement_refactoring_requests](svg/courses/ai/developing-using-ai/04_prompt_engineering/code_improvement_refactoring_requests.svg)

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

![anti_pattern_removal](svg/courses/ai/developing-using-ai/04_prompt_engineering/anti_pattern_removal.svg)

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

![step_by_step_instructions](svg/courses/ai/developing-using-ai/04_prompt_engineering/step_by_step_instructions.svg)

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

```
```template
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
## Context Window Management

![context_window_management](svg/courses/ai/developing-using-ai/04_prompt_engineering/context_window_management.svg)

---

## Prompt Length Optimization

Finding the sweet spot:

**Too Short**: Missing critical context
```markdown
"Fix this bug"
```

**Too Long**: Dilutes important information
```markdown
[500 lines of context for a simple question]
```

**Just Right**: Balanced and focused
```markdown
Context: Python web scraper using BeautifulSoup
Issue: Getting AttributeError on line 23
Code: [relevant 20 lines]
Task: Fix the error and explain why it occurred
```

---

## Prompt Versioning

Track what works:

```markdown
# v1.0 - Basic request
"Create a login function"

# v1.1 - Added specifications
"Create a login function with email/password"

# v1.2 - Added security requirements
"Create a secure login function with:
- Email/password validation
- Rate limiting
- SQL injection prevention"

# v1.3 - Added format requirements [BEST]
"Create a secure login function with:
- Email/password validation
- Rate limiting
- SQL injection prevention
Return: {success: bool, token?: string, error?: string}"
```

Document successful prompts for reuse

---

## Common Prompt Mistakes

![common_prompt_mistakes](svg/courses/ai/developing-using-ai/04_prompt_engineering/common_prompt_mistakes.svg)

---

## Prompt Debugging

When results aren't what you expected:

1. **Check specificity**: Is the request clear?
1. **Verify context**: Is all necessary information provided?
1. **Review constraints**: Are limitations clearly stated?
1. **Examine examples**: Do examples match expectations?
1. **Test incrementally**: Break complex prompts into parts
1. **Compare outputs**: Try variations to identify issues

Debug prompts like code - systematically

---

## Domain-Specific Prompting

Tailoring to your field:

**Frontend Development**:
```markdown
Create a React component for a data table with:
- TypeScript interfaces
- Styled-components
- Accessibility (ARIA labels)
- Mobile responsive
- Virtual scrolling for 10k+ rows
```

**Data Science**:
```markdown
Write a Python function using pandas to:
- Clean missing data (forward fill for time series)
- Detect outliers using IQR method
- Normalize using StandardScaler
- Return preprocessed DataFrame
Include docstring with parameter types
```

---

## Multi-Turn Prompt Strategies

Building on previous responses:

```markdown
Turn 1: "Create a basic Express server"
Turn 2: "Add authentication middleware using JWT"
Turn 3: "Now add rate limiting to the auth endpoints"
Turn 4: "Add comprehensive error handling"
Turn 5: "Finally, add logging with Winston"
```

Each turn builds on the previous, maintaining context

---

## Prompt Engineering for Different AI Models

![prompt_engineering_for_different_ai_models](svg/courses/ai/developing-using-ai/04_prompt_engineering/prompt_engineering_for_different_ai_models.svg)

---

## Measuring Prompt Effectiveness

Key metrics to track:

```markdown
Quality Metrics:
- Accuracy: Does output match requirements? ✓/✗
- Completeness: All requirements addressed? 1-10
- Clarity: Is the code/response clear? 1-10

Efficiency Metrics:
- Iterations needed: 1, 2, 3+
- Time to solution: Minutes
- Token usage: Input + Output

Success Rate:
- First-try success: 60%
- After refinement: 95%
- Complete failures: 5%
```

Track and improve your prompting skills

---

## Building a Prompt Library

Organize your successful prompts:

```markdown
📁 Prompt Library
  📁 Code Generation
    - function_template.md
    - class_template.md
    - api_endpoint.md
  📁 Debugging
    - error_analysis.md
    - performance_fix.md
    - security_audit.md
  📁 Documentation
    - api_docs.md
    - readme_generator.md
    - comment_creator.md
  📁 Testing
    - unit_test.md
    - integration_test.md
    - test_cases.md
```

---

## Real-World Prompt Examples

Production-ready prompts:

```markdown
# Microservice Generator
Create a Node.js microservice for {service_name} with:
- Express.js framework
- PostgreSQL with Sequelize ORM
- JWT authentication middleware
- Request validation using Joi
- Structured logging with Winston
- Health check endpoint
- Docker configuration
- Unit tests with Jest
- API documentation with Swagger

Include error handling, rate limiting, and CORS setup.
```

Use as template, customize per need

---

## Prompt Engineering Best Practices

![prompt_engineering_best_practices](svg/courses/ai/developing-using-ai/04_prompt_engineering/prompt_engineering_best_practices.svg)

---

## Chapter Summary

**Key Takeaways**:

Prompt engineering is the critical skill for AI-assisted development

Mastered techniques:
    - Clear requirement specification with context
    - Structured output formatting
    - Iterative refinement strategies
    - Advanced techniques (chain-of-thought, few-shot)
    - Domain-specific prompting patterns

Better prompts = Better code = Less time wasted

---

## Next Steps

Coming up in following chapters:

1. **Chapter 5**: AI-Enhanced Coding Practices - TDD, refactoring, debugging
1. **Chapter 6**: Learning and Skill Development - accelerated growth
1. **Chapter 7**: Specialized Development Tasks - domain-specific AI
1. **Chapter 8**: Quality and Best Practices - maintaining standards

Ready to apply these prompting skills in practice!
