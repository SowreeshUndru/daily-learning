# MySQL CASE Statement

`CASE` in MySQL is like an **if-else statement**. It lets you return different values based on different conditions.

> **Important:** `CASE` is **not** a SQL clause like `WHERE` or `GROUP BY`. It is an **expression** that returns **one value for every row**.

---

# Syntax

## 1. Searched CASE (Most Common)

```sql
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ...
    ELSE default_result
END
```

---

## 2. Simple CASE

Compares one expression against multiple values.

```sql
CASE expression
    WHEN value1 THEN result1
    WHEN value2 THEN result2
    ELSE default_result
END
```

---

# How CASE Works (The Most Important Concept)

Whenever SQL encounters a `CASE` expression, you can imagine that it creates a **temporary (virtual) column**.

> It **does not** create a new row.
>
> It computes **one value for every existing row**, forming a virtual column that exists only while the query is executing.

For example,

```sql
CASE
    WHEN salary >= 50000 THEN 'High'
    ELSE 'Low'
END
```

Suppose the table is:

| Name | Salary |
|------|--------|
| A | 60000 |
| B | 30000 |
| C | 80000 |

SQL internally behaves **as if** it created this temporary column:

| Name | Salary | Virtual Category |
|------|--------|------------------|
| A | 60000 | High |
| B | 30000 | Low |
| C | 80000 | High |

This virtual column is then used by whichever SQL clause contains the `CASE`.

---

# CASE Does Not Have Its Own Execution Stage

One of the biggest misconceptions is thinking that `CASE` has its own position in SQL's execution order.

It **does not**.

`CASE` is simply an **expression**, just like:

```sql
salary + 1000
```

or

```sql
UPPER(name)
```

It is evaluated **when the clause containing it is executed**.

For example:

- Inside `SELECT` → evaluated during the `SELECT` stage.
- Inside `WHERE` → evaluated during the `WHERE` stage.
- Inside `GROUP BY` → evaluated during the `GROUP BY` stage.
- Inside `ORDER BY` → evaluated during the `ORDER BY` stage.
- Inside `SUM()` → evaluated while `SUM()` processes each row.

Think of it this way:

> **CASE doesn't execute first.**
>
> The clause executes first, and if that clause contains a `CASE`, SQL evaluates it there.

---

# 1. CASE in SELECT

Classify employees based on salary.

```sql
SELECT
    name,
    salary,
    CASE
        WHEN salary >= 100000 THEN 'High'
        WHEN salary >= 50000 THEN 'Medium'
        ELSE 'Low'
    END AS salary_level
FROM Employee;
```

### Output

| Name | Salary | Salary Level |
|------|--------|--------------|
| A | 120000 | High |
| B | 70000 | Medium |
| C | 30000 | Low |

### Internal Thinking

Imagine SQL creates this virtual column:

| Name | Salary | Salary Level |
|------|--------|--------------|
| A | 120000 | High |
| B | 70000 | Medium |
| C | 30000 | Low |

The `SELECT` clause simply displays that computed column.

---

# 2. CASE inside Aggregate Functions ⭐ (Very Common)

Count completed orders.

```sql
SELECT
    SUM(
        CASE
            WHEN status = 'completed' THEN 1
            ELSE 0
        END
    ) AS completed_orders
FROM Orders;
```

Internal evaluation:

| Status | CASE Result |
|---------|-------------|
| completed | 1 |
| pending | 0 |
| cancelled | 0 |
| completed | 1 |

Then

```
SUM(1 + 0 + 0 + 1)
```

Result:

```
2
```

---

## Count Cancelled Orders

```sql
SELECT
    COUNT(
        CASE
            WHEN status = 'cancelled' THEN 1
        END
    )
FROM Orders;
```

or more commonly

```sql
SELECT
    SUM(
        CASE
            WHEN status='cancelled' THEN 1
            ELSE 0
        END
    )
FROM Orders;
```

---

# 3. Conditional SUM

Find total salary of IT employees.

```sql
SELECT
    SUM(
        CASE
            WHEN dept='IT' THEN salary
            ELSE 0
        END
    ) AS total_it_salary
FROM Employee;
```

Virtual values:

| Dept | Salary | CASE Result |
|------|--------|-------------|
| IT | 50000 | 50000 |
| HR | 40000 | 0 |
| IT | 70000 | 70000 |

Then

```
SUM(50000 + 0 + 70000)
```

---

# 4. Conditional AVG

```sql
SELECT
    AVG(
        CASE
            WHEN dept='IT' THEN salary
        END
    ) AS avg_it_salary
FROM Employee;
```

Notice there is **no ELSE**.

When no condition matches, `CASE` returns **NULL**.

`AVG()` ignores NULL values.

Example:

| Dept | Salary | CASE Result |
|------|--------|-------------|
| IT | 50000 | 50000 |
| HR | 40000 | NULL |
| IT | 70000 | 70000 |

Average:

```
(50000 + 70000) / 2
```

---

# 5. CASE in WHERE

```sql
SELECT *
FROM Employee
WHERE
CASE
    WHEN dept='IT' THEN salary > 50000
    ELSE salary > 30000
END;
```

Although valid, it is rarely written like this.

### Internal Thinking

Suppose

| Dept | Salary |
|------|--------|
| IT | 60000 |
| IT | 45000 |
| HR | 35000 |
| HR | 25000 |

Virtual Boolean column:

| Dept | Salary | CASE Result |
|------|--------|-------------|
| IT | 60000 | TRUE |
| IT | 45000 | FALSE |
| HR | 35000 | TRUE |
| HR | 25000 | FALSE |

`WHERE` simply keeps rows where the result is **TRUE**.

Equivalent query:

```sql
SELECT *
FROM Employee
WHERE
(dept='IT' AND salary>50000)
OR
(dept<>'IT' AND salary>30000);
```

---

# 6. CASE in ORDER BY

```sql
SELECT *
FROM Employee
ORDER BY
CASE
    WHEN salary>=100000 THEN 1
    WHEN salary>=50000 THEN 2
    ELSE 3
END;
```

Imagine SQL creates this virtual sort key.

| Salary | Sort Key |
|--------|----------|
| 120000 | 1 |
| 75000 | 2 |
| 30000 | 3 |
| 150000 | 1 |
| 60000 | 2 |

`ORDER BY` simply sorts by this temporary column.

Result:

```
1
1
2
2
3
```

Notice that employees with the same sort key are **not guaranteed to be ordered by salary**.

If you also want that:

```sql
ORDER BY
CASE
    WHEN salary>=100000 THEN 1
    WHEN salary>=50000 THEN 2
    ELSE 3
END,
salary DESC;
```

---

# 7. CASE in GROUP BY

```sql
SELECT
    CASE
        WHEN salary>=50000 THEN 'High'
        ELSE 'Low'
    END AS category,
    COUNT(*)
FROM Employee
GROUP BY
CASE
    WHEN salary>=50000 THEN 'High'
    ELSE 'Low'
END;
```

Imagine SQL creates this virtual column.

| Name | Salary | Category |
|------|--------|----------|
| A | 60000 | High |
| B | 30000 | Low |
| C | 70000 | High |
| D | 25000 | Low |

`GROUP BY` groups rows using this temporary column.

```
High
----
A
C

Low
---
B
D
```

Then

```
COUNT(*)
```

is calculated for each group.

Output:

| Category | Count |
|----------|-------|
| High | 2 |
| Low | 2 |

---

# 8. CASE in HAVING

```sql
SELECT
    dept,
    SUM(salary) AS total_salary
FROM Employee
GROUP BY dept
HAVING
CASE
    WHEN SUM(salary)>500000 THEN TRUE
    ELSE FALSE
END;
```

Usually written simply as

```sql
HAVING SUM(salary) > 500000;
```

---

# 9. CASE with Window Functions

```sql
SELECT
    name,
    salary,
    ROW_NUMBER() OVER(
        PARTITION BY
            CASE
                WHEN salary>=50000 THEN 'High'
                ELSE 'Low'
            END
        ORDER BY salary DESC
    ) AS rn
FROM Employee;
```

The `CASE` expression creates a temporary partition key.

Rows are partitioned into:

```
High
Low
```

Then `ROW_NUMBER()` runs separately inside each partition.

---

# 10. Simple CASE

```sql
SELECT
    status,
    CASE status
        WHEN 'P' THEN 'Pending'
        WHEN 'C' THEN 'Completed'
        WHEN 'R' THEN 'Rejected'
        ELSE 'Unknown'
    END
FROM Orders;
```

Equivalent to

```sql
CASE
    WHEN status='P' THEN 'Pending'
    WHEN status='C' THEN 'Completed'
    WHEN status='R' THEN 'Rejected'
    ELSE 'Unknown'
END
```

---

# Most Common CASE Patterns in LeetCode & Interviews

## Count Conditionally

```sql
SUM(CASE WHEN condition THEN 1 ELSE 0 END)
```

---

## Sum Conditionally

```sql
SUM(CASE WHEN condition THEN amount ELSE 0 END)
```

---

## Average Conditionally

```sql
AVG(CASE WHEN condition THEN amount END)
```

---

## Maximum Conditionally

```sql
MAX(CASE WHEN condition THEN value END)
```

---

## Pivot Rows into Columns

```sql
SELECT
    SUM(CASE WHEN month='Jan' THEN sales ELSE 0 END) AS Jan,
    SUM(CASE WHEN month='Feb' THEN sales ELSE 0 END) AS Feb,
    SUM(CASE WHEN month='Mar' THEN sales ELSE 0 END) AS Mar
FROM Sales;
```

---

# Where Can CASE Be Used?

Since `CASE` is an **expression**, it can be used almost anywhere SQL expects a value.

✅ SELECT

✅ WHERE

✅ GROUP BY

✅ HAVING

✅ ORDER BY

✅ Aggregate Functions (`SUM`, `COUNT`, `AVG`, `MAX`, `MIN`)

✅ Window Functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`)

---

# SQL Execution Order with CASE

Remember the logical execution order:

```
FROM
↓
WHERE
↓
GROUP BY
↓
HAVING
↓
SELECT
↓
ORDER BY
```

`CASE` has **no separate execution stage**.

It is evaluated **inside whichever clause contains it**.

Examples:

```
SELECT CASE ...
```

The `CASE` executes during the `SELECT` stage.

```
WHERE CASE ...
```

The `CASE` executes during the `WHERE` stage.

```
ORDER BY CASE ...
```

The `CASE` executes during the `ORDER BY` stage.

---

# Mental Model

Whenever you see a `CASE`, imagine SQL creating a **temporary (virtual) column**.

Examples:

```
CASE
WHEN salary>=50000 THEN 'High'
ELSE 'Low'
END
```

Imagine:

| Salary | Virtual Value |
|---------|---------------|
| 60000 | High |
| 30000 | Low |
| 70000 | High |

Then:

- `SELECT` displays it.
- `WHERE` filters using it.
- `GROUP BY` groups using it.
- `ORDER BY` sorts using it.
- Aggregate functions (`SUM`, `COUNT`, etc.) compute over it.

The virtual column exists **only during query execution**. It is **never stored in the table**.

---

# Rule to Remember

> **CASE computes one value per row.**

Think of it as creating a **temporary virtual column**.

The SQL clause containing the `CASE` decides what to do with those computed values:

- **SELECT** → Display them.
- **WHERE** → Filter rows.
- **GROUP BY** → Group rows.
- **ORDER BY** → Sort rows.
- **HAVING** → Filter groups.
- **SUM / COUNT / AVG / MAX / MIN** → Aggregate those values.
- **Window Functions** → Partition or rank using those values.

---

# Interview Pattern to Remember ⭐

The most frequently used `CASE` pattern in coding interviews and LeetCode is:

```sql
SUM(CASE WHEN condition THEN 1 ELSE 0 END)
```

because it efficiently counts rows satisfying a condition in a single pass.