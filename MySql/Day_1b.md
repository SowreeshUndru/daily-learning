# SQL Aggregate Functions vs Window Functions (`OVER`)

## 1. Aggregate Functions

Aggregate functions operate on a group of rows and return **one value per group**.

Common aggregate functions:

* `SUM()`
* `AVG()`
* `COUNT()`
* `MAX()`
* `MIN()`

### Example Table

| name | dept | salary |
| ---- | ---- | ------ |
| A    | IT   | 1000   |
| B    | IT   | 2000   |
| C    | IT   | 3000   |
| D    | HR   | 4000   |
| E    | HR   | 5000   |

---

## Aggregate Without `GROUP BY`

```sql
SELECT SUM(salary)
FROM Employee;
```

Output:

| SUM(salary) |
| ----------- |
| 15000       |

Since there is **no `GROUP BY`**, SQL treats the **entire table as one group**.

The same is true for:

```sql
SELECT AVG(salary) FROM Employee;
SELECT COUNT(*) FROM Employee;
SELECT MAX(salary) FROM Employee;
SELECT MIN(salary) FROM Employee;
```

Each returns **one row**.

---

## Aggregate With `GROUP BY`

```sql
SELECT dept, SUM(salary)
FROM Employee
GROUP BY dept;
```

Output:

| dept | SUM(salary) |
| ---- | ----------- |
| IT   | 6000        |
| HR   | 9000        |

Now SQL creates one group for each department.

---

## Why This Doesn't Work?

```sql
SELECT name, AVG(salary)
FROM Employee;
```

❌ Invalid

Reason:

`AVG(salary)` produces one value, but SQL doesn't know which `name` to display.

To make it valid:

```sql
SELECT name, AVG(salary)
FROM Employee
GROUP BY name;
```

**Rule:**

Every non-aggregated column in the `SELECT` list must appear in the `GROUP BY` clause.

---

# Window Functions (`OVER()`)

Unlike `GROUP BY`, window functions **do not reduce the number of rows**.

They compute a value and attach it to every row.

Syntax:

```sql
FUNCTION(...) OVER(...)
```

---

# `PARTITION BY`

`PARTITION BY` divides the rows into groups.

The aggregate is computed separately for each partition, but **all rows remain in the output**.

Example:

```sql
SELECT
    name,
    dept,
    salary,
    SUM(salary) OVER (PARTITION BY dept) AS dept_total
FROM Employee;
```

Output:

| name | dept | salary | dept_total |
| ---- | ---- | ------ | ---------- |
| A    | IT   | 1000   | 6000       |
| B    | IT   | 2000   | 6000       |
| C    | IT   | 3000   | 6000       |
| D    | HR   | 4000   | 9000       |
| E    | HR   | 5000   | 9000       |

Notice:

* Rows are **not collapsed**.
* SQL computes the department total once.
* That total is repeated for every row in that department.

---

# `PARTITION BY` + `ORDER BY`

When an `ORDER BY` is added inside `OVER()`, most aggregate window functions become **running (cumulative) aggregates**.

Example:

```sql
SELECT
    name,
    dept,
    salary,
    SUM(salary) OVER (
        PARTITION BY dept
        ORDER BY salary
    ) AS running_total
FROM Employee;
```

Output:

| name | dept | salary | running_total |
| ---- | ---- | ------ | ------------- |
| A    | IT   | 1000   | 1000          |
| B    | IT   | 2000   | 3000          |
| C    | IT   | 3000   | 6000          |
| D    | HR   | 4000   | 4000          |
| E    | HR   | 5000   | 9000          |

The calculation starts from the first row in each partition and continues to the current row.

---

# `COUNT()` as a Window Function

Without `ORDER BY`

```sql
COUNT(*) OVER (PARTITION BY dept)
```

Output:

| dept | count |
| ---- | ----- |
| IT   | 3     |
| IT   | 3     |
| IT   | 3     |
| HR   | 2     |
| HR   | 2     |

With `ORDER BY`

```sql
COUNT(*) OVER (
    PARTITION BY dept
    ORDER BY salary
)
```

Output:

| dept | running_count |
| ---- | ------------- |
| IT   | 1             |
| IT   | 2             |
| IT   | 3             |
| HR   | 1             |
| HR   | 2             |

---

# `AVG()` as a Window Function

Without `ORDER BY`

```sql
AVG(salary) OVER (PARTITION BY dept)
```

Output:

| dept | average |
| ---- | ------- |
| IT   | 2000    |
| IT   | 2000    |
| IT   | 2000    |
| HR   | 4500    |
| HR   | 4500    |

With `ORDER BY`

```sql
AVG(salary) OVER (
    PARTITION BY dept
    ORDER BY salary
)
```

Running averages:

| salary | running_avg |
| ------ | ----------- |
| 1000   | 1000        |
| 2000   | 1500        |
| 3000   | 2000        |

---

# Summary Table

| Query                                                 | Rows Returned          | Result                                                    |
| ----------------------------------------------------- | ---------------------- | --------------------------------------------------------- |
| `SUM(salary)`                                         | 1                      | Total salary of the table                                 |
| `SUM(salary) GROUP BY dept`                           | One row per department | Total salary for each department                          |
| `SUM(salary) OVER()`                                  | Same number of rows    | Total salary repeated on every row                        |
| `SUM(salary) OVER(PARTITION BY dept)`                 | Same number of rows    | Department total repeated on every row in that department |
| `SUM(salary) OVER(PARTITION BY dept ORDER BY salary)` | Same number of rows    | Running (cumulative) department total                     |

---

# Difference Between `GROUP BY` and `OVER()`

| `GROUP BY`                                 | `OVER()`                        |
| ------------------------------------------ | ------------------------------- |
| Reduces rows                               | Keeps all rows                  |
| Returns one row per group                  | Returns one value for every row |
| Used for summaries                         | Used for analytics              |
| Cannot access original rows after grouping | Original rows remain available  |
| Aggregate computed once per group          | Aggregate attached to each row  |

---

# Interview Tip

Remember this simple rule:

* **Aggregate Function** → Returns **one value per group**.
* **Window Function** → Returns **one value per row**.

Without `ORDER BY`:

```sql
SUM() OVER(PARTITION BY dept)
```

→ Entire partition sum repeated for every row.

With `ORDER BY`:

```sql
SUM() OVER(
    PARTITION BY dept
    ORDER BY salary
)
```

→ Running (cumulative) sum.

The same behavior applies to:

* `SUM()`
* `COUNT()`
* `AVG()`

and similar aggregate window functions.
