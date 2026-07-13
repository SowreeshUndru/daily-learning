# `OVER()` Clause Notes (Window Functions)

The `OVER()` clause is used with **window functions**.

It tells SQL **how to partition and order the rows** for the window function.

---

## Syntax

```sql
FUNCTION(...) OVER (
    PARTITION BY ...
    ORDER BY ...
    ROWS BETWEEN ...
)
```

---

# What is Allowed Inside `OVER()`

### 1. PARTITION BY

Splits rows into partitions (windows).

```sql
COUNT(*) OVER (
    PARTITION BY department
)
```

---

### 2. ORDER BY

Defines the order of rows within each partition.

```sql
ROW_NUMBER() OVER (
    ORDER BY salary DESC
)
```

---

### 3. ROWS / RANGE

Defines the window frame.

```sql
SUM(salary) OVER (
    ORDER BY id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

---

# What is NOT Allowed Inside `OVER()`

## ❌ WHERE

```sql
COUNT(*) OVER (
    WHERE status = 'cancelled'
)
```

**Reason:**
`WHERE` filters rows before window functions are applied.

---

## ❌ GROUP BY

```sql
COUNT(*) OVER (
    GROUP BY department
)
```

**Reason:**
`GROUP BY` creates groups and collapses rows.
Window functions do **not** collapse rows.

---

## ❌ HAVING

```sql
COUNT(*) OVER (
    HAVING COUNT(*) > 2
)
```

**Reason:**
`HAVING` filters groups after `GROUP BY`.
Window functions work on rows, not grouped results.

---

# Difference Between `PARTITION BY` and `GROUP BY`

## GROUP BY

- Creates groups.
- Returns **one row per group**.
- Used with aggregate functions.

Example:

```sql
SELECT department,
       COUNT(*)
FROM Employees
GROUP BY department;
```

Output:

| Department | Count |
|------------|-------|
| HR | 5 |
| IT | 8 |

---

## PARTITION BY

- Creates partitions (windows).
- **Does NOT reduce the number of rows.**
- Every row is still returned.

Example:

```sql
SELECT *,
       COUNT(*) OVER (
           PARTITION BY department
       ) AS dept_count
FROM Employees;
```

Output:

| Employee | Department | dept_count |
|----------|------------|------------|
| A | HR | 5 |
| B | HR | 5 |
| C | IT | 8 |
| D | IT | 8 |

Notice that every employee is still present.

---

# Easy Way to Remember

## `GROUP BY`

- Groups rows
- Returns one row per group

## `PARTITION BY`

- Creates windows
- Keeps every row

---

# Interview Memory Trick

Think of `OVER()` as answering:

> **"How should I divide and order the rows for this window function?"**

It **does not** decide:

- Which rows to keep (`WHERE`)
- How to create grouped results (`GROUP BY`)
- Which groups to keep (`HAVING`)

---

# Summary

| Clause | Allowed Inside `OVER()`? |
|---------|--------------------------|
| PARTITION BY | ✅ Yes |
| ORDER BY | ✅ Yes |
| ROWS / RANGE | ✅ Yes |
| WHERE | ❌ No |
| GROUP BY | ❌ No |
| HAVING | ❌ No |

---

# One-Line Memory Trick

> **`OVER()` defines the window. It does NOT filter rows (`WHERE`), create groups (`GROUP BY`), or filter groups (`HAVING`).**





# SQL Interview Note: Top N Records Per Group Using Window Functions

## Question

**Suppose I have three classes: Class A, Class B, and Class C.**

I want to retrieve the **top 3 students (highest marks)** from **each class**.

Can I write something like this?

```sql
SELECT *,
       RANK() OVER (
           PARTITION BY class
           ORDER BY marks DESC
       ) AS rnk
FROM Students
WHERE rnk <= 3;
```

---

## Answer

❌ **No. This query is not valid.**

Reason:

The alias `rnk` is created using a **window function**, but the `WHERE` clause is executed **before** window functions are calculated.

Therefore, when SQL reaches:

```sql
WHERE rnk <= 3
```

the column `rnk` **does not exist yet**.

---

# SQL Execution Order

```text
FROM
WHERE
GROUP BY
HAVING
WINDOW FUNCTIONS (OVER)
SELECT
ORDER BY
LIMIT
```

Notice:

- `WHERE` executes **before**
- `RANK() OVER(...)` is calculated **later**

So SQL cannot filter using `rnk` directly.

---

# Correct Solution

Use a **subquery** (or a CTE).

```sql
SELECT *
FROM (
    SELECT *,
           RANK() OVER (
               PARTITION BY class
               ORDER BY marks DESC
           ) AS rnk
    FROM Students
) t
WHERE rnk <= 3;
```

---

# Step-by-Step Execution

## Original Data

| Class | Student | Marks |
|-------|---------|------:|
| A | John | 95 |
| A | Alice | 90 |
| A | Bob | 88 |
| A | Tom | 85 |
| B | Sam | 98 |
| B | Joe | 92 |
| B | Mary | 90 |

---

## Step 1: Compute the Rank

The subquery executes first.

```sql
SELECT *,
       RANK() OVER (
           PARTITION BY class
           ORDER BY marks DESC
       ) AS rnk
FROM Students;
```

Result:

| Class | Student | Marks | rnk |
|-------|---------|------:|----:|
| A | John | 95 | 1 |
| A | Alice | 90 | 2 |
| A | Bob | 88 | 3 |
| A | Tom | 85 | 4 |
| B | Sam | 98 | 1 |
| B | Joe | 92 | 2 |
| B | Mary | 90 | 3 |

---

## Step 2: Filter the Result

Now the outer query executes.

```sql
WHERE rnk <= 3
```

Result:

| Class | Student | Marks | rnk |
|-------|---------|------:|----:|
| A | John | 95 | 1 |
| A | Alice | 90 | 2 |
| A | Bob | 88 | 3 |
| B | Sam | 98 | 1 |
| B | Joe | 92 | 2 |
| B | Mary | 90 | 3 |

These are the **Top 3 students from each class**.

---

# Why Does This Work?

The execution order becomes:

```text
Inner Query
-----------
FROM Students
↓
Calculate RANK() OVER(...)
↓
Create a temporary table containing 'rnk'

Outer Query
-----------
Read the temporary table
↓
WHERE rnk <= 3
↓
Return the final result
```

Now `rnk` already exists, so filtering is possible.

---

# Alternative Using CTE

```sql
WITH RankedStudents AS (
    SELECT *,
           RANK() OVER (
               PARTITION BY class
               ORDER BY marks DESC
           ) AS rnk
    FROM Students
)

SELECT *
FROM RankedStudents
WHERE rnk <= 3;
```

This is equivalent to the subquery and is often easier to read.

---

# Common Interview Pattern

Whenever you need to filter based on:

- `ROW_NUMBER()`
- `RANK()`
- `DENSE_RANK()`
- `NTILE()`
- `LAG()`
- `LEAD()`

follow this pattern:

```sql
SELECT *
FROM (
    SELECT *,
           WINDOW_FUNCTION() OVER (...) AS alias
    FROM table_name
) t
WHERE alias <condition>;
```

---

# Interview Trick

Ask yourself:

> **Am I filtering using a window function?**

If **Yes**, then:

- ❌ Don't use `WHERE` directly.
- ✅ First compute the window function in a subquery or CTE.
- ✅ Then filter in the outer query.

---

# One-Line Memory Trick

> **Window functions are computed after `WHERE`, so you must first calculate them (using a subquery or CTE) and then filter their results.**



````md
# SQL Notes: Top 3 Students from Each Class and Section

## Question

Suppose I have:

- Class A, B, C
- Each class has Sections 1, 2, 3
- Each section has many students

I want to find the **Top 3 students (highest marks)** from **every section of every class**.

---

## Solution

```sql
SELECT *
FROM (
    SELECT *,
           RANK() OVER (
               PARTITION BY class, section
               ORDER BY marks DESC
           ) AS rnk
    FROM Students
) t
WHERE rnk <= 3;
```

---

## How `PARTITION BY` Works

### `PARTITION BY class`

Ranking restarts for every class.

```
Class A
--------
Rank 1
Rank 2
Rank 3
...

Class B
--------
Rank 1
Rank 2
Rank 3
...

Class C
--------
Rank 1
Rank 2
Rank 3
...
```

---

### `PARTITION BY class, section`

Ranking restarts for every **Class + Section** combination.

```
Class A - Section 1
-------------------
Rank 1
Rank 2
Rank 3
...

Class A - Section 2
-------------------
Rank 1
Rank 2
Rank 3
...

Class B - Section 1
-------------------
Rank 1
Rank 2
Rank 3
...

Class C - Section 3
-------------------
Rank 1
Rank 2
Rank 3
...
```

Each section gets its own ranking.

---

## General Rule

### One column

```sql
PARTITION BY class
```

→ Restart ranking for every class.

---

### Two columns

```sql
PARTITION BY class, section
```

→ Restart ranking for every Class + Section.

---

### Three columns

```sql
PARTITION BY class, section, subject
```

→ Restart ranking for every Class + Section + Subject.

---

## Memory Trick

> **`PARTITION BY` means "Restart the window function whenever these column values change."**

Examples:

- `PARTITION BY class`
  - Restart for each class.

- `PARTITION BY class, section`
  - Restart for each class-section.

- `PARTITION BY department, team`
  - Restart for each department-team.

---

## Interview Tip

If the question says:

- Top 3 students **per class**
- Highest salary **per department**
- Top 5 products **per category**
- Highest scorer **per team**

👉 Think **`PARTITION BY`**.

If there are multiple groups (like Class + Section), simply include all of them:

```sql
PARTITION BY class, section
```
````
