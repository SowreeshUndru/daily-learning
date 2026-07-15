# Common Table Expression (CTE)

A **Common Table Expression (CTE)** is a **temporary named result set** that is created using the `WITH` keyword. You can think of it as a **temporary table** that exists only while a single SQL statement is executing. Once that SQL statement finishes, the CTE is automatically removed by the database.

## Syntax

```sql
WITH cte_name AS (
    SELECT ...
)
main_query;
```

The `main_query` can be a `SELECT`, `INSERT`, `UPDATE`, or `DELETE`.

---

## Example 1: Basic CTE

```sql
WITH HighSalary AS (
    SELECT *
    FROM Employee
    WHERE salary > 50000
)

SELECT *
FROM HighSalary;
```

In this example, `HighSalary` is the CTE. The database first executes the query inside the CTE, creates a temporary result set, and then the `SELECT` statement reads from it. After the query finishes, `HighSalary` no longer exists.

---

## Using a CTE Multiple Times

A CTE can be referenced multiple times **as long as it is within the same SQL statement**.

```sql
WITH HighSalary AS (
    SELECT *
    FROM Employee
    WHERE salary > 50000
)

SELECT
    (SELECT COUNT(*) FROM HighSalary) AS total,
    (SELECT AVG(salary) FROM HighSalary) AS average_salary,
    (SELECT MAX(salary) FROM HighSalary) AS highest_salary;
```

Here, the same CTE (`HighSalary`) is used three times to calculate the total number of employees, the average salary, and the maximum salary. Since all of these references are part of a single SQL statement, the CTE is available to all of them.

---

## Scope of a CTE

A CTE is available **only within the SQL statement in which it is defined**.

✅ Valid

```sql
WITH Temp AS (
    SELECT *
    FROM Employee
)

SELECT * FROM Temp;
```

❌ Invalid

```sql
WITH Temp AS (
    SELECT *
    FROM Employee
)

SELECT * FROM Temp;

SELECT COUNT(*) FROM Temp;
```

The second `SELECT` will produce an error because the first SQL statement has already finished, so the CTE has been automatically removed.

---

## When to Use a CTE

Use a CTE when:
- You want to make a complex query easier to read.
- You want to avoid writing deeply nested subqueries.
- You need to reuse the same intermediate result multiple times within a single SQL statement.
- You want to break a large query into smaller, more understandable parts.