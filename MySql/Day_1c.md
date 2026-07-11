# SQL Notes - Dependent (Correlated) Subquery

## What is a Dependent (Correlated) Subquery?

A **dependent subquery** (also called a **correlated subquery**) is an **inner query** that depends on the **outer query** for its values.

The inner query **cannot execute independently** because it references one or more columns from the outer query.

---

## Example

Find employees whose salary is greater than the average salary of their own department.

```sql
SELECT e1.name,
       e1.salary
FROM Employee e1
WHERE e1.salary > (
    SELECT AVG(e2.salary)
    FROM Employee e2
    WHERE e2.departmentId = e1.departmentId
);
```

---

# How the Query Executes

Assume the `Employee` table contains:

| Name | Salary | Department |
|------|--------|------------|
| Alice| 7000   | 1          |
| Bob  | 5000   | 1          |
|Charlie| 9000  | 2          |
| David | 6000  | 2          |

---

### Step 1: The Outer Query Starts

The database begins executing the **outer query**.

```sql
SELECT e1.name,
       e1.salary
FROM Employee e1
```

At this point, **no filtering has happened yet**. The outer query starts reading employees **one row at a time**.

---

### Step 2: Outer Query Reads the First Row

Current row:

```
Name = Alice
Salary = 7000
Department = 1
```

The outer query now reaches the `WHERE` condition.

```sql
WHERE e1.salary > (Inner Query)
```

To evaluate this condition, it must execute the **inner query**.

---

### Step 3: The Inner Query Executes

The inner query uses the department of the current employee (`Department = 1`).

So it becomes:

```sql
SELECT AVG(salary)
FROM Employee
WHERE departmentId = 1;
```

Result:

```
Average Salary = 6000
```

Now the outer query compares:

```
7000 > 6000
```

Result:

```
TRUE
```

Alice is included in the output.

---

### Step 4: Outer Query Reads the Next Row

Current row:

```
Name = Bob
Salary = 5000
Department = 1
```

Again, the outer query reaches the `WHERE` condition.

The **inner query executes again** because the outer query is now processing a different row.

```sql
SELECT AVG(salary)
FROM Employee
WHERE departmentId = 1;
```

Result:

```
Average Salary = 6000
```

Comparison:

```
5000 > 6000
```

Result:

```
FALSE
```

Bob is not included.

---

### Step 5: Outer Query Reads the Third Row

Current row:

```
Name = Charlie
Salary = 9000
Department = 2
```

The inner query executes again.

```sql
SELECT AVG(salary)
FROM Employee
WHERE departmentId = 2;
```

Result:

```
Average Salary = 7500
```

Comparison:

```
9000 > 7500
```

Result:

```
TRUE
```

Charlie is included.

---

### Step 6: The Process Continues

The outer query continues reading rows one by one.

For **every row**, the **inner query executes again** using the values of that current row.

This continues until the outer query has processed every employee.

---

## Execution Flow

```
Outer Query Starts
        │
        ▼
Read First Row
        │
        ▼
Execute Inner Query
        │
        ▼
Evaluate WHERE Condition
        │
        ▼
Return or Skip Row
        │
        ▼
Read Next Row
        │
        ▼
Execute Inner Query Again
        │
        ▼
Repeat Until All Rows Are Processed
```

> **Remember:** The **outer query** processes one row at a time, and for **each row**, the **inner query** is executed again. This repeated execution is what makes it a **dependent (correlated) subquery**.

