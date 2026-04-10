# Prompt Engineering for Developers

---

## Prompt Engineering Formula

![Prompt Engineering Formula](svg/courses/ai/developing-using-ai-short/04_prompt_engineering/prompt_formula.svg)

---

## The Art and Science of AI Communication

Master the language that makes AI understand exactly what you need

This chapter covers:
1. Fundamentals of effective prompting
1. Code generation prompts
1. Debugging and problem-solving prompts
1. Advanced prompting techniques

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

## Clear Requirement Specification

**Poor**: "Create a user function"

**Better**: "Create a Python function to validate user registration"

**Best**:
```markdown
Create a Python function that validates user registration with:
- Email format validation
- Password strength check (8+ chars, 1 uppercase, 1 number)
- Username uniqueness check against database
- Return validation errors as a dictionary
- Use type hints and docstrings
```

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

## Code Generation Templates

### Function Generation
```markdown
Create a [language] function with these specifications:

Function name: processUserData
Purpose: Filter and transform user data
Parameters:
- userData: array of user objects
- options: configuration object (optional)

Returns: Processed user array

Requirements:
- Input validation
- Error handling for missing fields
- Performance: O(n) complexity
- Include documentation
```

---

## Algorithm Implementation Prompts

```markdown
Implement the quicksort algorithm in Python:

Requirements:
- Time complexity: O(n log n) average
- Space complexity: O(log n) for recursion
- Handle edge cases: empty array, single element, duplicates
- Include comments explaining key steps
- Add type hints

Example:
Input: [3, 1, 4, 1, 5, 9, 2, 6]
Output: [1, 1, 2, 3, 4, 5, 6, 9]
```

---

## API Endpoint Design

```markdown
Design a REST API endpoint for user authentication:

Method: POST
Path: /api/v1/auth/login

Request Body:
{
  "email": "string",
  "password": "string",
  "remember_me": "boolean (optional)"
}

Response codes:
- 200: Success with JWT token
- 401: Invalid credentials
- 429: Rate limited

Include:
- Input validation
- Secure password checking
- JWT generation
- Error response format
```

---

## Debugging Prompts

Effective debugging requests:

```markdown
Debug this error:

Error message: TypeError: Cannot read property 'map' of undefined
Code causing error: items.map(item => <Item key={item.id} />)
Context: React component rendering a list
Environment: React 18, TypeScript

What I've tried:
1. Console logging items - shows undefined
2. Adding default props - didn't help

Expected: Render list of items
Actual: Component crashes

Please explain root cause and provide fix.
```

---

## Performance Optimization

```markdown
Optimize this function for speed:

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
3. Password security
4. Session management
5. Input validation

Provide:
- Identified vulnerabilities with severity
- Fixed code with explanations
- Security best practices checklist
```

---

## Advanced Techniques

### Chain-of-Thought
```markdown
Solve this step by step:

Problem: Design a distributed task queue system

Think through:
1. First, identify core requirements
2. Then, consider architecture components
3. Next, evaluate message broker options
4. After that, design worker pool strategy
5. Finally, describe monitoring approach

Show reasoning at each step before providing solution.
```

### Few-Shot Examples
```markdown
Convert SQL to MongoDB:

Example 1:
SQL: SELECT * FROM users WHERE age > 25
MongoDB: db.users.find({ age: { $gt: 25 } })

Example 2:
SQL: SELECT name FROM users WHERE status = 'active'
MongoDB: db.users.find({ status: 'active' }, { name: 1 })

Now convert:
SELECT * FROM orders WHERE total > 100 AND status IN ('pending', 'processing')
```

---

## Role-Based Prompting

```markdown
Act as a senior DevOps engineer with 10 years of experience.

Review this Kubernetes deployment configuration:
[paste YAML config]

Evaluate for:
- Security best practices
- Resource optimization
- High availability
- Scalability concerns

Provide recommendations as you would in a production review.
```

---

## Iterative Refinement Process

1. **Initial Prompt**: Basic request
1. **AI Response**: First attempt
1. **Evaluate**: Check if it meets needs
1. **Refine Prompt**: Add missing details
1. **Iterate**: Until optimal result

Example:
```markdown
v1: "Create a login function"
v2: "Create a secure login function with email/password"
v3: "Create a secure login function with:
    - Email/password validation
    - Rate limiting
    - SQL injection prevention
    - Return JWT token on success"
```

---

## Common Prompt Mistakes

### Avoid These Pitfalls

❌ **Ambiguous Requirements**
"Make it better" → "Optimize for performance, target 100ms response time"

❌ **Missing Context**
"Fix this bug" → "Fix this React rendering bug in a TypeScript project"

❌ **No Success Criteria**
"Improve the code" → "Refactor to reduce complexity from 15 to under 10"

❌ **Assuming AI Knowledge**
"Use the usual pattern" → "Use the Repository pattern with dependency injection"

---

## Prompt Templates Library

### Bug Fix Template
```markdown
Error: {error_message}
Code: {code_snippet}
Context: {tech_stack}
Expected: {expected_behavior}
Actual: {actual_behavior}
Fix the issue and explain the cause.
```

### Optimization Template
```markdown
Optimize this {code_type} for {metric}:
{code}
Current: {current_metric}
Target: {target_metric}
Constraints: {limitations}
```

### Review Template
```markdown
Review this {language} code:
{code}
Focus on: {priorities}
Check for: security, performance, maintainability
```

---

## Measuring Prompt Effectiveness

Track these metrics:

**Quality Metrics**:
- Accuracy: Does output match requirements?
- Completeness: All requirements addressed?
- Clarity: Is the code/response clear?

**Efficiency Metrics**:
- Iterations needed: 1, 2, 3+
- Time to solution: Minutes
- Success rate: First-try success %

Use metrics to improve your prompting skills

---

## Chapter Summary

**Key Takeaways**:

Prompt engineering is the critical skill for AI-assisted development

Master these essentials:
- The CONTEXT + TASK + CONSTRAINTS + FORMAT + EXAMPLES formula
- Clear requirement specification
- Iterative refinement strategies
- Advanced techniques (chain-of-thought, few-shot, role-based)

Better prompts = Better code = Less time wasted

Next: AI-Enhanced Coding Practices
