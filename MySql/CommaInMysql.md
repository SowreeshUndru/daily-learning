# MySQL Comma (`,`) Usage Notes

## Rule to Remember

A comma **always separates items**. What those items are depends on the SQL statement.

There are **two categories**:

1. **Separating data/items (keyword written once)**
2. **Separating operations/actions (each operation must be complete)**

---

# 1. Comma Separating Columns (Keyword Written Once)

## SELECT

The comma separates the columns to retrieve.

```sql
SELECT id, name, salary
FROM Employee;
```

Only one `SELECT` is needed.

---

## ORDER BY

The comma separates sorting columns.

```sql
ORDER BY departmentId, salary DESC, name;
```

Meaning:

1. Sort by `departmentId`
2. If department is same → sort by `salary DESC`
3. If both are same → sort by `name`

Only one `ORDER BY` is needed because there is only one sorting operation.

---

## GROUP BY

```sql
GROUP BY departmentId, salary;
```

The comma separates grouping columns.

Only one `GROUP BY` is required.

---

## PARTITION BY

```sql
DENSE_RANK() OVER(
    PARTITION BY departmentId, salary
    ORDER BY id
)
```

The comma separates partition columns.

---

## DISTINCT

```sql
SELECT DISTINCT departmentId, salary
FROM Employee;
```

The comma separates the columns that together determine uniqueness.

---

## INSERT Column List

```sql
INSERT INTO Employee(id, name, salary)
VALUES (1, 'John', 50000);
```

The comma separates column names.

---

## VALUES

### Single row

```sql
VALUES (1, 'John', 50000);
```

### Multiple rows

```sql
INSERT INTO Employee(id, name)
VALUES
(1, 'John'),
(2, 'Alice'),
(3, 'Bob');
```

The comma separates rows.

---

## UPDATE SET

```sql
UPDATE Employee
SET salary = 60000,
    departmentId = 2
WHERE id = 1;
```

The comma separates column assignments.

---

## Function Arguments

```sql
CONCAT(firstName, lastName);
```

```sql
ROUND(price, 2);
```

```sql
SUBSTRING(name, 2, 3);
```

The comma separates function arguments.

---

# 2. Comma Separating Operations (Each Operation Must Be Complete)

These statements perform **actions**.

Each action must be written completely.

---

## ALTER TABLE

### Correct

```sql
ALTER TABLE Employee
ADD COLUMN age INT,
DROP COLUMN salary,
MODIFY COLUMN name VARCHAR(100);
```

Three separate operations:

- ADD COLUMN
- DROP COLUMN
- MODIFY COLUMN

---

### Wrong

```sql
ALTER TABLE Employee
DROP COLUMN age,
email;
```

**Why?**

After the comma, MySQL expects another complete operation.

`email` is only a column name, not an operation.

---

### Correct

```sql
ALTER TABLE Employee
DROP COLUMN age,
DROP COLUMN email;
```

---

## Multiple ADD

### Correct

```sql
ALTER TABLE Employee
ADD COLUMN age INT,
ADD COLUMN email VARCHAR(100);
```

### Wrong

```sql
ALTER TABLE Employee
ADD COLUMN age INT,
email VARCHAR(100);
```

---

## Multiple MODIFY

```sql
ALTER TABLE Employee
MODIFY COLUMN age BIGINT,
MODIFY COLUMN salary DECIMAL(10,2);
```

---

## Multiple CHANGE

```sql
ALTER TABLE Employee
CHANGE COLUMN age emp_age INT,
CHANGE COLUMN salary emp_salary DECIMAL(10,2);
```

---

# Why ORDER BY Doesn't Repeat

```sql
ORDER BY departmentId, salary DESC;
```

The comma separates **columns**.

There is only **one sorting operation**, so `ORDER BY` is written once.

---

# Why ALTER TABLE Repeats

```sql
ALTER TABLE Employee
DROP COLUMN age,
DROP COLUMN salary;
```

The comma separates **operations**.

Each operation must be complete.

---

# Compare Them

## SELECT

```sql
SELECT id, name, salary;
```

Think:

```
Retrieve:
- id
- name
- salary
```

One operation → retrieve columns.

---

## ORDER BY

```sql
ORDER BY departmentId, salary;
```

Think:

```
Sort by:
- departmentId
- salary
```

One sorting operation.

---

## ALTER TABLE

```sql
ALTER TABLE Employee
ADD COLUMN age INT,
DROP COLUMN salary;
```

Think:

```
Operation 1 → Add column
Operation 2 → Drop column
```

Two different operations.

---

# Semicolon vs Comma

## Comma (,)

Separates items **inside one SQL statement**.

Example:

```sql
SELECT id, name, salary;
```

---

## Semicolon (;)

Ends one SQL statement and starts another.

```sql
SELECT * FROM Employee;

SELECT * FROM Department;
```

---

# Quick Reference Table

| SQL Clause | Comma Separates | Keyword Repeated? |
|------------|-----------------|-------------------|
| `SELECT` | Columns | ❌ No |
| `INSERT INTO (...)` | Columns | ❌ No |
| `VALUES (...)` | Values / Rows | ❌ No |
| `UPDATE SET` | Column assignments | ❌ No |
| `ORDER BY` | Sorting columns | ❌ No |
| `GROUP BY` | Grouping columns | ❌ No |
| `PARTITION BY` | Partition columns | ❌ No |
| `DISTINCT` | Unique columns | ❌ No |
| Function calls | Function arguments | ❌ No |
| `ALTER TABLE` | Alter operations | ✅ Yes (`ADD`, `DROP`, `MODIFY`, `CHANGE`) |

---

# Memory Trick

### When the comma separates **things**, write the keyword only once.

Examples:

```sql
SELECT id, name, salary;
```

```sql
ORDER BY salary DESC, name;
```

```sql
GROUP BY departmentId, salary;
```

---

### When the comma separates **actions**, every action must be complete.

```sql
ALTER TABLE Employee
ADD COLUMN age INT,
DROP COLUMN salary,
MODIFY COLUMN name VARCHAR(100);
```

---

# One-Line Rule

> **Comma separates items.**
>
> - If the items are **columns, values, or expressions**, the keyword is written **once**.
> - If the items are **operations/actions**, every operation must be written **completely**.