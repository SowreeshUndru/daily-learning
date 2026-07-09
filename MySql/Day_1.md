# 185. Department Top Three Salaries

## Problem

Given two tables:

### Employee

| Column | Type |
|--------|------|
| id | int |
| name | varchar |
| salary | int |
| departmentId | int |

### Department

| Column | Type |
|--------|------|
| id | int |
| name | varchar |

Find all employees whose salary is among the **top 3 unique salaries** in their respective departments.

> **Note:** If multiple employees have the same salary, they should all be included.

---

## Approach

- Use the `DENSE_RANK()` window function.
- Partition employees by `departmentId`.
- Rank salaries in descending order within each department.
- Keep only employees whose rank is **less than or equal to 3**.
- Join with the `Department` table to display department names.

---

## SQL Solution

```sql
SELECT
    d.name AS Department,
    e.name AS Employee,
    e.salary AS Salary
FROM (
    SELECT *,
           DENSE_RANK() OVER (
               PARTITION BY departmentId
               ORDER BY salary DESC
           ) AS rk
    FROM Employee
) AS e
JOIN Department d
ON e.departmentId = d.id
WHERE rk <= 3;
```

---

## Explanation

### Step 1: Rank salaries within each department

```sql
DENSE_RANK() OVER (
    PARTITION BY departmentId
    ORDER BY salary DESC
)
```

- `PARTITION BY departmentId` → Creates separate groups for each department.
- `ORDER BY salary DESC` → Ranks salaries from highest to lowest.
- `DENSE_RANK()` → Assigns the same rank to equal salaries without skipping ranks.

Example:

| Department | Salary | Rank |
|------------|--------|------|
| IT | 9000 | 1 |
| IT | 9000 | 1 |
| IT | 8500 | 2 |
| IT | 8000 | 3 |
| IT | 7000 | 4 |

---

### Step 2: Filter top 3 salaries

```sql
WHERE rk <= 3
```

Keeps only employees whose salary belongs to the top three unique salaries in their department.

---

### Step 3: Join with Department

```sql
JOIN Department d
ON e.departmentId = d.id
```

Retrieves the department name for the final output.

---

## Time Complexity

- Ranking employees: **O(n log n)**
- Join operation: **O(n)**

Overall: **O(n log n)**

---

## Key Concept

Use **`DENSE_RANK()`** instead of `RANK()` because the problem asks for the **top 3 unique salaries**.

- `RANK()` skips ranks after ties.
- `DENSE_RANK()` does **not** skip ranks, making it the correct choice.