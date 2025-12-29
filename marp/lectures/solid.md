# SOLID Principles
## Understanding the Foundation of Object-Oriented Design
---
## Overview
1. Single Responsibility Principle (SRP)
1. Open/Closed Principle (OCP)
1. Liskov Substitution Principle (LSP)
1. Interface Segregation Principle (ISP)
1. Dependency Inversion Principle (DIP)
---
## Why SOLID?
- Maintainable code
- Easier testing
- Flexible architecture
- Reduced technical debt
- Better scalability
- Easier to understand and modify
---
## Single Responsibility Principle

> "A class should have one, and only one, reason to change."
> - Robert C. Martin

---
## SRP - Bad Example

```java
class Employee {
    private String name;
    private double salary;

    public void calculatePay() { /* ... */ }
    public void saveToDatabase() { /* ... */ }
    public void generateReport() { /* ... */ }
    public void sendEmail() { /* ... */ }
}
```

---
## SRP - Violation Visualization

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="50" width="300" height="200" fill="#f0f4f8" stroke="#2563eb" stroke-width="2"/>
  <text x="400" y="80" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Employee</text>
  <line x1="250" y1="90" x2="550" y2="90" stroke="#2563eb" stroke-width="1"/>
  <text x="260" y="110" font-family="Arial" font-size="12">- name: String</text>
  <text x="260" y="130" font-family="Arial" font-size="12">- salary: double</text>
  <line x1="250" y1="140" x2="550" y2="140" stroke="#2563eb" stroke-width="1"/>
  <text x="260" y="160" font-family="Arial" font-size="12">+ calculatePay()</text>
  <text x="260" y="180" font-family="Arial" font-size="12">+ saveToDatabase()</text>
  <text x="260" y="200" font-family="Arial" font-size="12">+ generateReport()</text>
  <text x="260" y="220" font-family="Arial" font-size="12">+ sendEmail()</text>

  <rect x="50" y="300" width="120" height="40" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="110" y="325" text-anchor="middle" font-family="Arial" font-size="12">PayrollDepartment</text>

  <rect x="250" y="300" width="80" height="40" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="290" y="325" text-anchor="middle" font-family="Arial" font-size="12">HR</text>

  <rect x="410" y="300" width="100" height="40" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="460" y="325" text-anchor="middle" font-family="Arial" font-size="12">Reporting</text>

  <rect x="590" y="300" width="80" height="40" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="630" y="325" text-anchor="middle" font-family="Arial" font-size="12">IT</text>

  <line x1="170" y1="300" x2="350" y2="250" stroke="#dc2626" stroke-width="1" stroke-dasharray="5,5"/>
  <line x1="290" y1="300" x2="380" y2="250" stroke="#dc2626" stroke-width="1" stroke-dasharray="5,5"/>
  <line x1="460" y1="300" x2="430" y2="250" stroke="#dc2626" stroke-width="1" stroke-dasharray="5,5"/>
  <line x1="590" y1="320" x2="480" y2="250" stroke="#dc2626" stroke-width="1" stroke-dasharray="5,5"/>

  <text x="400" y="380" text-anchor="middle" font-family="Arial" font-size="11" fill="#dc2626">Multiple responsibilities = Violation of SRP</text>
</svg>

---
## SRP - Good Example

```java
class Employee {
    private String name;
    private double salary;
}

class PayrollCalculator {
    public void calculatePay(Employee employee) { /* ... */ }
}

class EmployeeRepository {
    public void save(Employee employee) { /* ... */ }
}

class ReportGenerator {
    public void generateReport(Employee employee) { /* ... */ }
}

class EmailService {
    public void sendEmail(String to, String content) { /* ... */ }
}
```

---
## SRP - Better Structure

<svg viewBox="0 0 900 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="350" y="50" width="200" height="100" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="450" y="80" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Employee</text>
  <line x1="350" y1="90" x2="550" y2="90" stroke="#16a34a" stroke-width="1"/>
  <text x="360" y="110" font-family="Arial" font-size="12">- name: String</text>
  <text x="360" y="130" font-family="Arial" font-size="12">- salary: double</text>

  <rect x="50" y="250" width="160" height="80" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="130" y="280" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">PayrollCalculator</text>
  <line x1="50" y1="290" x2="210" y2="290" stroke="#0284c7" stroke-width="1"/>
  <text x="60" y="310" font-family="Arial" font-size="12">+ calculatePay(Employee)</text>

  <rect x="250" y="250" width="160" height="80" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="330" y="280" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">EmployeeRepository</text>
  <line x1="250" y1="290" x2="410" y2="290" stroke="#0284c7" stroke-width="1"/>
  <text x="260" y="310" font-family="Arial" font-size="12">+ save(Employee)</text>

  <rect x="450" y="250" width="160" height="80" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="530" y="280" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">ReportGenerator</text>
  <line x1="450" y1="290" x2="610" y2="290" stroke="#0284c7" stroke-width="1"/>
  <text x="460" y="310" font-family="Arial" font-size="12">+ generateReport(Employee)</text>

  <rect x="650" y="250" width="180" height="80" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="740" y="280" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">EmailService</text>
  <line x1="650" y1="290" x2="830" y2="290" stroke="#0284c7" stroke-width="1"/>
  <text x="660" y="310" font-family="Arial" font-size="12">+ sendEmail(String, String)</text>

  <line x1="130" y1="250" x2="400" y2="150" stroke="#16a34a" stroke-width="1" marker-end="url(#arrowhead)"/>
  <line x1="330" y1="250" x2="430" y2="150" stroke="#16a34a" stroke-width="1" marker-end="url(#arrowhead)"/>
  <line x1="530" y1="250" x2="470" y2="150" stroke="#16a34a" stroke-width="1" marker-end="url(#arrowhead)"/>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#16a34a"/>
    </marker>
  </defs>

  <text x="450" y="400" text-anchor="middle" font-family="Arial" font-size="11" fill="#16a34a">Single Responsibility: Each class has one job</text>
</svg>

---
## Open/Closed Principle

> "Software entities should be open for extension, but closed for modification."
> - Bertrand Meyer

---
## OCP - Bad Example

```java
class Rectangle {
    private double width;
    private double height;
    // getters, setters
}

class AreaCalculator {
    public double calculateArea(Object shape) {
        if (shape instanceof Rectangle) {
            Rectangle rect = (Rectangle) shape;
            return rect.getWidth() * rect.getHeight();
        }
        else if (shape instanceof Circle) {
            Circle circle = (Circle) shape;
            return Math.PI * circle.getRadius() * circle.getRadius();
        }
        return 0;
    }
}
```

---
## OCP - Violation Visualization

<svg viewBox="0 0 700 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="50" width="200" height="60" fill="#fee2e2" stroke="#dc2626" stroke-width="2" rx="5"/>
  <text x="350" y="85" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">AreaCalculator</text>

  <rect x="50" y="200" width="100" height="50" fill="#f0f4f8" stroke="#64748b" stroke-width="2" rx="5"/>
  <text x="100" y="230" text-anchor="middle" font-family="Arial" font-size="14">Rectangle</text>

  <rect x="200" y="200" width="100" height="50" fill="#f0f4f8" stroke="#64748b" stroke-width="2" rx="5"/>
  <text x="250" y="230" text-anchor="middle" font-family="Arial" font-size="14">Circle</text>

  <rect x="350" y="200" width="100" height="50" fill="#f0f4f8" stroke="#64748b" stroke-width="2" rx="5"/>
  <text x="400" y="230" text-anchor="middle" font-family="Arial" font-size="14">Triangle</text>

  <rect x="500" y="200" width="130" height="50" fill="#fef3c7" stroke="#f59e0b" stroke-width="2" rx="5" stroke-dasharray="5,5"/>
  <text x="565" y="230" text-anchor="middle" font-family="Arial" font-size="14">Future Shapes...</text>

  <path d="M 300 110 L 100 200" stroke="#dc2626" stroke-width="2" marker-end="url(#arrow-red)"/>
  <text x="180" y="155" font-family="Arial" font-size="11" fill="#dc2626">instanceof</text>

  <path d="M 330 110 L 250 200" stroke="#dc2626" stroke-width="2" marker-end="url(#arrow-red)"/>
  <text x="280" y="155" font-family="Arial" font-size="11" fill="#dc2626">instanceof</text>

  <path d="M 370 110 L 400 200" stroke="#dc2626" stroke-width="2" marker-end="url(#arrow-red)"/>
  <text x="380" y="155" font-family="Arial" font-size="11" fill="#dc2626">instanceof</text>

  <path d="M 420 110 L 565 200" stroke="#f59e0b" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrow-orange)"/>
  <text x="480" y="155" font-family="Arial" font-size="11" fill="#f59e0b">instanceof</text>

  <defs>
    <marker id="arrow-red" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#dc2626"/>
    </marker>
    <marker id="arrow-orange" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#f59e0b"/>
    </marker>
  </defs>

  <text x="350" y="320" text-anchor="middle" font-family="Arial" font-size="11" fill="#dc2626">Must modify AreaCalculator for each new shape</text>
  <text x="350" y="340" text-anchor="middle" font-family="Arial" font-size="11" fill="#dc2626">Violation of Open/Closed Principle</text>
</svg>

---
## OCP - Good Example

```java
interface Shape {
    double calculateArea();
}

class Rectangle implements Shape {
    private double width;
    private double height;

    public double calculateArea() {
        return width * height;
    }
}

class Circle implements Shape {
    private double radius;

    public double calculateArea() {
        return Math.PI * radius * radius;
    }
}
```

---
## OCP - Better Structure

<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="50" width="200" height="80" fill="#e0f2fe" stroke="#0284c7" stroke-width="2" rx="5" stroke-dasharray="5,5"/>
  <text x="300" y="75" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">«interface»</text>
  <text x="300" y="95" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Shape</text>
  <line x1="200" y1="105" x2="400" y2="105" stroke="#0284c7" stroke-width="1"/>
  <text x="300" y="120" text-anchor="middle" font-family="Arial" font-size="12">+ calculateArea(): double</text>

  <rect x="80" y="220" width="180" height="120" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="170" y="250" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Rectangle</text>
  <line x1="80" y1="260" x2="260" y2="260" stroke="#16a34a" stroke-width="1"/>
  <text x="90" y="280" font-family="Arial" font-size="12">- width: double</text>
  <text x="90" y="300" font-family="Arial" font-size="12">- height: double</text>
  <line x1="80" y1="310" x2="260" y2="310" stroke="#16a34a" stroke-width="1"/>
  <text x="90" y="330" font-family="Arial" font-size="12">+ calculateArea(): double</text>

  <rect x="340" y="220" width="180" height="120" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="430" y="250" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Circle</text>
  <line x1="340" y1="260" x2="520" y2="260" stroke="#16a34a" stroke-width="1"/>
  <text x="350" y="280" font-family="Arial" font-size="12">- radius: double</text>
  <line x1="340" y1="310" x2="520" y2="310" stroke="#16a34a" stroke-width="1"/>
  <text x="350" y="330" font-family="Arial" font-size="12">+ calculateArea(): double</text>

  <path d="M 170 220 L 280 130" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="280,130 275,140 285,140" fill="none" stroke="#16a34a" stroke-width="2"/>

  <path d="M 430 220 L 320 130" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="320,130 315,140 325,140" fill="none" stroke="#16a34a" stroke-width="2"/>

  <text x="300" y="380" text-anchor="middle" font-family="Arial" font-size="11" fill="#16a34a">Open for extension, closed for modification</text>
</svg>

---
## Liskov Substitution Principle

> "Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program."
> - Barbara Liskov

---
## LSP - Bad Example

```java
class Bird {
    public void fly() {
        // Implementation
    }
}

class Penguin extends Bird {
    @Override
    public void fly() {
        throw new UnsupportedOperationException("Penguins can't fly!");
    }
}
```

---
## LSP - Violation Visualization

<svg viewBox="0 0 700 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="100" height="300" fill="#f0f4f8" stroke="#64748b" stroke-width="1"/>
  <text x="100" y="80" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">Client</text>

  <rect x="300" y="50" width="100" height="300" fill="#f0f4f8" stroke="#64748b" stroke-width="1"/>
  <text x="350" y="80" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">Bird</text>

  <rect x="500" y="50" width="100" height="300" fill="#f0f4f8" stroke="#64748b" stroke-width="1"/>
  <text x="550" y="80" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">Penguin</text>

  <line x1="150" y1="120" x2="300" y2="120" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow-green)"/>
  <text x="225" y="110" text-anchor="middle" font-family="Arial" font-size="11">fly()</text>

  <line x1="350" y1="140" x2="350" y2="160" stroke="#16a34a" stroke-width="2"/>
  <rect x="320" y="160" width="60" height="30" fill="#dcfce7" stroke="#16a34a" stroke-width="1" rx="3"/>
  <text x="350" y="180" text-anchor="middle" font-family="Arial" font-size="10">Flies</text>
  <text x="350" y="190" text-anchor="middle" font-family="Arial" font-size="10">successfully</text>

  <line x1="150" y1="250" x2="500" y2="250" stroke="#dc2626" stroke-width="2" marker-end="url(#arrow-red)"/>
  <text x="325" y="240" text-anchor="middle" font-family="Arial" font-size="11">fly()</text>

  <line x1="550" y1="270" x2="150" y2="270" stroke="#dc2626" stroke-width="2" marker-end="url(#arrow-red)" stroke-dasharray="5,5"/>

  <rect x="180" y="280" width="200" height="40" fill="#fee2e2" stroke="#dc2626" stroke-width="1" rx="3"/>
  <text x="280" y="295" text-anchor="middle" font-family="Arial" font-size="11" font-weight="bold">Throws Exception!</text>
  <text x="280" y="310" text-anchor="middle" font-family="Arial" font-size="10">UnsupportedOperationException</text>

  <defs>
    <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#16a34a"/>
    </marker>
    <marker id="arrow-red" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#dc2626"/>
    </marker>
  </defs>

  <text x="350" y="370" text-anchor="middle" font-family="Arial" font-size="11" fill="#dc2626">Penguin cannot be substituted for Bird - LSP Violation</text>
</svg>

---
## LSP - Good Example

```java
interface Bird {
    void move();
}

interface FlyingBird extends Bird {
    void fly();
}

class Sparrow implements FlyingBird {
    public void move() { /* ... */ }
    public void fly() { /* ... */ }
}

class Penguin implements Bird {
    public void move() { /* ... */ }
}
```

---
## LSP - Better Structure

<svg viewBox="0 0 700 450" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="50" width="150" height="70" fill="#e0f2fe" stroke="#0284c7" stroke-width="2" rx="5" stroke-dasharray="5,5"/>
  <text x="325" y="75" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">«interface»</text>
  <text x="325" y="95" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Bird</text>
  <line x1="250" y1="100" x2="400" y2="100" stroke="#0284c7" stroke-width="1"/>
  <text x="325" y="115" text-anchor="middle" font-family="Arial" font-size="12">+ move()</text>

  <rect x="450" y="140" width="150" height="90" fill="#e0f2fe" stroke="#0284c7" stroke-width="2" rx="5" stroke-dasharray="5,5"/>
  <text x="525" y="165" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">«interface»</text>
  <text x="525" y="185" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">FlyingBird</text>
  <line x1="450" y1="195" x2="600" y2="195" stroke="#0284c7" stroke-width="1"/>
  <text x="525" y="210" text-anchor="middle" font-family="Arial" font-size="12">+ move()</text>
  <text x="525" y="225" text-anchor="middle" font-family="Arial" font-size="12">+ fly()</text>

  <rect x="380" y="280" width="120" height="100" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="440" y="305" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Sparrow</text>
  <line x1="380" y1="315" x2="500" y2="315" stroke="#16a34a" stroke-width="1"/>
  <text x="390" y="335" font-family="Arial" font-size="12">+ move()</text>
  <text x="390" y="355" font-family="Arial" font-size="12">+ fly()</text>

  <rect x="150" y="280" width="120" height="100" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="210" y="305" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Penguin</text>
  <line x1="150" y1="315" x2="270" y2="315" stroke="#16a34a" stroke-width="1"/>
  <text x="160" y="335" font-family="Arial" font-size="12">+ move()</text>

  <path d="M 400 120 L 450 140" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-blue)"/>

  <path d="M 440 280 L 500 230" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="500,230 495,240 505,240" fill="none" stroke="#16a34a" stroke-width="2"/>

  <path d="M 210 280 L 290 120" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="290,120 285,130 295,130" fill="none" stroke="#16a34a" stroke-width="2"/>

  <defs>
    <marker id="arrow-blue" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#0284c7"/>
    </marker>
  </defs>

  <text x="350" y="420" text-anchor="middle" font-family="Arial" font-size="11" fill="#16a34a">Correct hierarchy - Penguins can substitute Birds</text>
  <text x="350" y="435" text-anchor="middle" font-family="Arial" font-size="11" fill="#16a34a">Sparrows can substitute FlyingBirds</text>
</svg>

---
## Interface Segregation Principle

> "Clients should not be forced to depend upon interfaces that they do not use."
> - Robert C. Martin

---
## ISP - Bad Example

```java
interface Worker {
    void work();
    void eat();
    void sleep();
}

class Human implements Worker {
    public void work() { /* ... */ }
    public void eat() { /* ... */ }
    public void sleep() { /* ... */ }
}

class Robot implements Worker {
    public void work() { /* ... */ }
    public void eat() { throw new UnsupportedOperationException(); }
    public void sleep() { throw new UnsupportedOperationException(); }
}
```

---
## ISP - Violation Visualization

<svg viewBox="0 0 700 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="50" width="150" height="110" fill="#fee2e2" stroke="#dc2626" stroke-width="2" rx="5" stroke-dasharray="5,5"/>
  <text x="325" y="75" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">«interface»</text>
  <text x="325" y="95" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Worker</text>
  <line x1="250" y1="105" x2="400" y2="105" stroke="#dc2626" stroke-width="1"/>
  <text x="325" y="120" text-anchor="middle" font-family="Arial" font-size="12">+ work()</text>
  <text x="325" y="135" text-anchor="middle" font-family="Arial" font-size="12">+ eat()</text>
  <text x="325" y="150" text-anchor="middle" font-family="Arial" font-size="12">+ sleep()</text>

  <rect x="100" y="240" width="150" height="110" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="175" y="265" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Human</text>
  <line x1="100" y1="275" x2="250" y2="275" stroke="#16a34a" stroke-width="1"/>
  <text x="175" y="295" text-anchor="middle" font-family="Arial" font-size="12">+ work()</text>
  <text x="175" y="310" text-anchor="middle" font-family="Arial" font-size="12">+ eat()</text>
  <text x="175" y="325" text-anchor="middle" font-family="Arial" font-size="12">+ sleep()</text>

  <rect x="400" y="240" width="180" height="110" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="490" y="265" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Robot</text>
  <line x1="400" y1="275" x2="580" y2="275" stroke="#f59e0b" stroke-width="1"/>
  <text x="490" y="295" text-anchor="middle" font-family="Arial" font-size="12">+ work()</text>
  <text x="420" y="310" font-family="Arial" font-size="12">+ eat()</text>
  <text x="530" y="310" font-family="Arial" font-size="12" fill="#dc2626">✗ Exception</text>
  <text x="420" y="325" font-family="Arial" font-size="12">+ sleep()</text>
  <text x="530" y="325" font-family="Arial" font-size="12" fill="#dc2626">✗ Exception</text>

  <path d="M 175 240 L 290 160" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="290,160 285,170 295,170" fill="none" stroke="#16a34a" stroke-width="2"/>

  <path d="M 490 240 L 360 160" stroke="#f59e0b" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="360,160 355,170 365,170" fill="none" stroke="#f59e0b" stroke-width="2"/>

  <text x="325" y="380" text-anchor="middle" font-family="Arial" font-size="11" fill="#dc2626">Robot forced to implement unnecessary methods - ISP Violation</text>
</svg>

---
## ISP - Good Example

```java
interface Workable {
    void work();
}

interface Eatable {
    void eat();
}

interface Sleepable {
    void sleep();
}

class Human implements Workable, Eatable, Sleepable {
    public void work() { /* ... */ }
    public void eat() { /* ... */ }
    public void sleep() { /* ... */ }
}

class Robot implements Workable {
    public void work() { /* ... */ }
}
```

---
## ISP - Better Structure

<svg viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="120" height="60" fill="#e0f2fe" stroke="#0284c7" stroke-width="2" rx="5" stroke-dasharray="5,5"/>
  <text x="160" y="70" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic">«interface»</text>
  <text x="160" y="85" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">Workable</text>
  <line x1="100" y1="90" x2="220" y2="90" stroke="#0284c7" stroke-width="1"/>
  <text x="160" y="105" text-anchor="middle" font-family="Arial" font-size="11">+ work()</text>

  <rect x="300" y="50" width="120" height="60" fill="#e0f2fe" stroke="#0284c7" stroke-width="2" rx="5" stroke-dasharray="5,5"/>
  <text x="360" y="70" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic">«interface»</text>
  <text x="360" y="85" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">Eatable</text>
  <line x1="300" y1="90" x2="420" y2="90" stroke="#0284c7" stroke-width="1"/>
  <text x="360" y="105" text-anchor="middle" font-family="Arial" font-size="11">+ eat()</text>

  <rect x="500" y="50" width="120" height="60" fill="#e0f2fe" stroke="#0284c7" stroke-width="2" rx="5" stroke-dasharray="5,5"/>
  <text x="560" y="70" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic">«interface»</text>
  <text x="560" y="85" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">Sleepable</text>
  <line x1="500" y1="90" x2="620" y2="90" stroke="#0284c7" stroke-width="1"/>
  <text x="560" y="105" text-anchor="middle" font-family="Arial" font-size="11">+ sleep()</text>

  <rect x="200" y="250" width="150" height="110" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="275" y="275" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Human</text>
  <line x1="200" y1="285" x2="350" y2="285" stroke="#16a34a" stroke-width="1"/>
  <text x="275" y="305" text-anchor="middle" font-family="Arial" font-size="12">+ work()</text>
  <text x="275" y="320" text-anchor="middle" font-family="Arial" font-size="12">+ eat()</text>
  <text x="275" y="335" text-anchor="middle" font-family="Arial" font-size="12">+ sleep()</text>

  <rect x="450" y="250" width="150" height="80" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="525" y="275" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Robot</text>
  <line x1="450" y1="285" x2="600" y2="285" stroke="#16a34a" stroke-width="1"/>
  <text x="525" y="305" text-anchor="middle" font-family="Arial" font-size="12">+ work()</text>

  <path d="M 160 110 L 240 250" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="240,250 235,240 245,240" fill="none" stroke="#16a34a" stroke-width="2"/>

  <path d="M 360 110 L 290 250" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="290,250 285,240 295,240" fill="none" stroke="#16a34a" stroke-width="2"/>

  <path d="M 560 110 L 310 250" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="310,250 305,240 315,240" fill="none" stroke="#16a34a" stroke-width="2"/>

  <path d="M 160 110 L 490 250" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="490,250 485,240 495,240" fill="none" stroke="#16a34a" stroke-width="2"/>

  <text x="400" y="410" text-anchor="middle" font-family="Arial" font-size="11" fill="#16a34a">Segregated interfaces - Classes only implement what they need</text>
  <text x="400" y="425" text-anchor="middle" font-family="Arial" font-size="11" fill="#16a34a">No forced implementations or exceptions</text>
</svg>

---
## Dependency Inversion Principle

> "High-level modules should not depend on low-level modules. Both should depend on abstractions."
> - Robert C. Martin

---
## DIP - Bad Example

```java
class LightBulb {
    public void turnOn() { /* ... */ }
    public void turnOff() { /* ... */ }
}

class Switch {
    private LightBulb bulb;

    public Switch() {
        this.bulb = new LightBulb();
    }

    public void operate() {
        // Direct dependency on LightBulb implementation
        bulb.turnOn();
    }
}
```

---
## DIP - Violation Visualization

<svg viewBox="0 0 600 350" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="100" width="180" height="100" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="190" y="130" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Switch</text>
  <line x1="100" y1="140" x2="280" y2="140" stroke="#dc2626" stroke-width="1"/>
  <text x="110" y="160" font-family="Arial" font-size="12">- bulb: LightBulb</text>
  <line x1="100" y1="170" x2="280" y2="170" stroke="#dc2626" stroke-width="1"/>
  <text x="110" y="190" font-family="Arial" font-size="12">+ operate()</text>

  <rect x="380" y="100" width="150" height="100" fill="#f0f4f8" stroke="#64748b" stroke-width="2"/>
  <text x="455" y="130" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">LightBulb</text>
  <line x1="380" y1="140" x2="530" y2="140" stroke="#64748b" stroke-width="1"/>
  <text x="390" y="160" font-family="Arial" font-size="12">+ turnOn()</text>
  <text x="390" y="180" font-family="Arial" font-size="12">+ turnOff()</text>

  <path d="M 280 150 L 380 150" stroke="#dc2626" stroke-width="2" marker-end="url(#arrow-red-direct)"/>

  <defs>
    <marker id="arrow-red-direct" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#dc2626"/>
    </marker>
  </defs>

  <text x="315" y="280" text-anchor="middle" font-family="Arial" font-size="11" fill="#dc2626">Direct dependency on concrete class</text>
  <text x="315" y="295" text-anchor="middle" font-family="Arial" font-size="11" fill="#dc2626">High-level module depends on low-level module</text>
  <text x="315" y="310" text-anchor="middle" font-family="Arial" font-size="11" fill="#dc2626">Violation of Dependency Inversion Principle</text>
</svg>

---
## DIP - Good Example

```java
interface Switchable {
    void turnOn();
    void turnOff();
}

class LightBulb implements Switchable {
    public void turnOn() { /* ... */ }
    public void turnOff() { /* ... */ }
}

class Switch {
    private final Switchable device;

    public Switch(Switchable device) {
        this.device = device;
    }

    public void operate() {
        device.turnOn();
    }
}
```

---
## DIP - Better Structure

<svg viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg">
  <rect x="300" y="50" width="150" height="80" fill="#e0f2fe" stroke="#0284c7" stroke-width="2" rx="5" stroke-dasharray="5,5"/>
  <text x="375" y="75" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">«interface»</text>
  <text x="375" y="95" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Switchable</text>
  <line x1="300" y1="105" x2="450" y2="105" stroke="#0284c7" stroke-width="1"/>
  <text x="375" y="120" text-anchor="middle" font-family="Arial" font-size="12">+ turnOn()</text>
  <text x="375" y="135" text-anchor="middle" font-family="Arial" font-size="12">+ turnOff()</text>

  <rect x="50" y="200" width="180" height="100" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="140" y="230" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Switch</text>
  <line x1="50" y1="240" x2="230" y2="240" stroke="#16a34a" stroke-width="1"/>
  <text x="60" y="260" font-family="Arial" font-size="12">- device: Switchable</text>
  <line x1="50" y1="270" x2="230" y2="270" stroke="#16a34a" stroke-width="1"/>
  <text x="60" y="290" font-family="Arial" font-size="12">+ operate()</text>

  <rect x="320" y="300" width="150" height="100" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="395" y="330" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">LightBulb</text>
  <line x1="320" y1="340" x2="470" y2="340" stroke="#16a34a" stroke-width="1"/>
  <text x="330" y="360" font-family="Arial" font-size="12">+ turnOn()</text>
  <text x="330" y="380" font-family="Arial" font-size="12">+ turnOff()</text>

  <rect x="520" y="300" width="150" height="100" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="595" y="330" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Fan</text>
  <line x1="520" y1="340" x2="670" y2="340" stroke="#16a34a" stroke-width="1"/>
  <text x="530" y="360" font-family="Arial" font-size="12">+ turnOn()</text>
  <text x="530" y="380" font-family="Arial" font-size="12">+ turnOff()</text>

  <path d="M 230 230 L 300 130" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow-green-dip)"/>

  <path d="M 395 300 L 375 150" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="375,150 370,160 380,160" fill="none" stroke="#16a34a" stroke-width="2"/>

  <path d="M 595 300 L 400 150" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="400,150 395,160 405,160" fill="none" stroke="#16a34a" stroke-width="2"/>

  <defs>
    <marker id="arrow-green-dip" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#16a34a"/>
    </marker>
  </defs>

  <text x="375" y="435" text-anchor="middle" font-family="Arial" font-size="11" fill="#16a34a">Both high-level and low-level modules depend on abstraction</text>
</svg>

---
## Real-World Example: E-commerce System

Let's see how SOLID principles work together in a real system.

---
## E-commerce System - Bad Design

```java
class Order {
    private List<Item> items;

    public void addItem(Item item) { /* ... */ }
    public void calculateTotal() { /* ... */ }
    public void processPayment() { /* ... */ }
    public void saveToDatabase() { /* ... */ }
    public void sendConfirmationEmail() { /* ... */ }
    public void generateInvoice() { /* ... */ }
}
```

---
## E-commerce - Bad Design Visualization

<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="100" width="300" height="200" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="300" y="130" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold">Order</text>
  <line x1="150" y1="140" x2="450" y2="140" stroke="#dc2626" stroke-width="1"/>
  <text x="160" y="160" font-family="Arial" font-size="12">- items: List&lt;Item&gt;</text>
  <line x1="150" y1="170" x2="450" y2="170" stroke="#dc2626" stroke-width="1"/>
  <text x="160" y="190" font-family="Arial" font-size="12">+ addItem(Item)</text>
  <text x="160" y="210" font-family="Arial" font-size="12">+ calculateTotal()</text>
  <text x="160" y="230" font-family="Arial" font-size="12">+ processPayment()</text>
  <text x="160" y="250" font-family="Arial" font-size="12">+ saveToDatabase()</text>
  <text x="160" y="270" font-family="Arial" font-size="12">+ sendConfirmationEmail()</text>
  <text x="160" y="290" font-family="Arial" font-size="12">+ generateInvoice()</text>

  <text x="300" y="50" text-anchor="middle" font-family="Arial" font-size="20" font-weight="bold" fill="#dc2626">God Class Anti-Pattern</text>

  <text x="300" y="340" text-anchor="middle" font-family="Arial" font-size="11" fill="#dc2626">Multiple responsibilities in a single class</text>
  <text x="300" y="355" text-anchor="middle" font-family="Arial" font-size="11" fill="#dc2626">Violates: SRP, OCP, DIP</text>
  <text x="300" y="370" text-anchor="middle" font-family="Arial" font-size="11" fill="#dc2626">Hard to test, maintain, and extend</text>
</svg>

---
## E-commerce System - SOLID Design

```java
interface OrderRepository {
    void save(Order order);
}

interface PaymentProcessor {
    void process(Order order);
}

interface NotificationService {
    void notify(Order order);
}

class Order {
    private List<Item> items;
    private final OrderCalculator calculator;

    public void addItem(Item item) { /* ... */ }
}

class OrderService {
    private final OrderRepository repository;
    private final PaymentProcessor paymentProcessor;
    private final NotificationService notificationService;

    public void processOrder(Order order) {
        paymentProcessor.process(order);
        repository.save(order);
        notificationService.notify(order);
    }
}
```

---
## E-commerce - SOLID Design Visualization

<svg viewBox="0 0 900 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="350" y="50" width="200" height="120" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="450" y="80" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">OrderService</text>
  <line x1="350" y1="90" x2="550" y2="90" stroke="#16a34a" stroke-width="1"/>
  <text x="360" y="110" font-family="Arial" font-size="11">- repository: OrderRepository</text>
  <text x="360" y="125" font-family="Arial" font-size="11">- paymentProcessor: PaymentProcessor</text>
  <text x="360" y="140" font-family="Arial" font-size="11">- notificationService: NotificationService</text>
  <line x1="350" y1="150" x2="550" y2="150" stroke="#16a34a" stroke-width="1"/>
  <text x="360" y="165" font-family="Arial" font-size="11">+ processOrder(Order)</text>

  <rect x="50" y="250" width="180" height="80" fill="#e0f2fe" stroke="#0284c7" stroke-width="2" rx="5" stroke-dasharray="5,5"/>
  <text x="140" y="270" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic">«interface»</text>
  <text x="140" y="290" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">OrderRepository</text>
  <line x1="50" y1="295" x2="230" y2="295" stroke="#0284c7" stroke-width="1"/>
  <text x="140" y="315" text-anchor="middle" font-family="Arial" font-size="11">+ save(Order)</text>

  <rect x="350" y="250" width="180" height="80" fill="#e0f2fe" stroke="#0284c7" stroke-width="2" rx="5" stroke-dasharray="5,5"/>
  <text x="440" y="270" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic">«interface»</text>
  <text x="440" y="290" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">PaymentProcessor</text>
  <line x1="350" y1="295" x2="530" y2="295" stroke="#0284c7" stroke-width="1"/>
  <text x="440" y="315" text-anchor="middle" font-family="Arial" font-size="11">+ process(Order)</text>

  <rect x="650" y="250" width="180" height="80" fill="#e0f2fe" stroke="#0284c7" stroke-width="2" rx="5" stroke-dasharray="5,5"/>
  <text x="740" y="270" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic">«interface»</text>
  <text x="740" y="290" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">NotificationService</text>
  <line x1="650" y1="295" x2="830" y2="295" stroke="#0284c7" stroke-width="1"/>
  <text x="740" y="315" text-anchor="middle" font-family="Arial" font-size="11">+ notify(Order)</text>

  <rect x="50" y="380" width="150" height="60" fill="#f0f4f8" stroke="#64748b" stroke-width="1"/>
  <text x="125" y="415" text-anchor="middle" font-family="Arial" font-size="12">MySQLRepository</text>

  <rect x="250" y="380" width="150" height="60" fill="#f0f4f8" stroke="#64748b" stroke-width="1"/>
  <text x="325" y="415" text-anchor="middle" font-family="Arial" font-size="12">StripeProcessor</text>

  <rect x="450" y="380" width="150" height="60" fill="#f0f4f8" stroke="#64748b" stroke-width="1"/>
  <text x="525" y="415" text-anchor="middle" font-family="Arial" font-size="12">PayPalProcessor</text>

  <rect x="650" y="380" width="150" height="60" fill="#f0f4f8" stroke="#64748b" stroke-width="1"/>
  <text x="725" y="415" text-anchor="middle" font-family="Arial" font-size="12">EmailNotification</text>

  <path d="M 380 170 L 140 250" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow-green-solid)"/>
  <path d="M 450 170 L 440 250" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow-green-solid)"/>
  <path d="M 520 170 L 740 250" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow-green-solid)"/>

  <path d="M 125 380 L 140 330" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <polygon points="140,330 135,340 145,340" fill="none" stroke="#64748b" stroke-width="1"/>

  <path d="M 325 380 L 410 330" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <polygon points="410,330 405,340 415,340" fill="none" stroke="#64748b" stroke-width="1"/>

  <path d="M 525 380 L 470 330" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <polygon points="470,330 465,340 475,340" fill="none" stroke="#64748b" stroke-width="1"/>

  <path d="M 725 380 L 740 330" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
  <polygon points="740,330 735,340 745,340" fill="none" stroke="#64748b" stroke-width="1"/>

  <defs>
    <marker id="arrow-green-solid" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#16a34a"/>
    </marker>
  </defs>

  <text x="450" y="475" text-anchor="middle" font-family="Arial" font-size="11" fill="#16a34a">SOLID Design: Separated concerns, dependency on abstractions, extensible</text>
</svg>

---
## Benefits of SOLID in the E-commerce Example
1. Single Responsibility: Each class has one job
1. Open/Closed: New payment methods without changing existing code
1. Liskov Substitution: Different repository implementations are interchangeable
1. Interface Segregation: Clients depend only on methods they need
1. Dependency Inversion: High-level OrderService depends on abstractions
---
## Common SOLID Violations
1. God Classes
1. Tight Coupling
1. Inheritance Abuse
1. Large Interfaces
1. Concrete Dependencies
---
## How to Identify SOLID Violations
1. Multiple responsibilities in one class
1. Frequent changes to existing code
1. Inheritance breaking functionality
1. Unused interface methods
1. Direct instantiation of dependencies
---
## Refactoring Towards SOLID
1. Extract Class
1. Extract Interface
1. Dependency Injection
1. Interface Segregation
1. Abstract Factory Pattern
---
## Testing Benefits with SOLID
- Easier unit testing
- Better mock objects
- Isolated components
- Focused test cases
- Improved test coverage
---
## Best Practices
1. Keep classes small and focused
1. Use composition over inheritance
1. Program to interfaces
1. Inject dependencies
1. Follow the Law of Demeter
---
## Common Questions
1. When to break SOLID principles?
1. How to balance SOLID with pragmatism?
1. What about performance impact?
1. How to handle legacy code?
1. Where to start applying SOLID?
---
## Tools and Techniques
1. Static Code Analysis
1. Design Pattern Recognition
1. Dependency Injection Frameworks
1. Refactoring IDEs
1. Architecture Validation Tools
---
## Summary
SOLID Principles:
1. Single Responsibility
1. Open/Closed
1. Liskov Substitution
1. Interface Segregation
1. Dependency Inversion
---
## Additional Resources
1. Clean Code by Robert C. Martin
1. Design Patterns by Gang of Four
1. Refactoring by Martin Fowler
1. Online courses and tutorials
1. Community discussions
