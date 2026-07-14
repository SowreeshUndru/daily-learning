# WHERE vs GROUP BY vs HAVING

Understanding the execution order of SQL is the key to writing correct queries.

---

## SQL Execution Order

``` 
FROM
JOIN
ON
WHERE
GROUP BY
Aggregate Functions (COUNT, SUM, AVG, MIN, MAX, ...)
HAVING
WINDOW FUNCTIONS (OVER, ROW_NUMBER, RANK, LAG, LEAD, ...)
SELECT
DISTINCT
ORDER BY
LIMIT / OFFSET
```

---

# WHERE

`WHERE` filters **individual rows** **before** grouping happens.

### Example

```sql
SELECT request_at, COUNT(*)
FROM Trips
WHERE status = 'cancelled'
GROUP BY request_at;
```

### Execution

```
Rows
   │
   ▼
WHERE (Filter rows)
   │
   ▼
GROUP BY (Create groups)
   │
   ▼
COUNT(*)
```

### Use WHERE when filtering using normal columns.

Examples:

```sql
WHERE banned = 'No'

WHERE age > 18

WHERE city = 'Delhi'

WHERE request_at BETWEEN '2013-10-01' AND '2013-10-03'
```

---

# GROUP BY

`GROUP BY` groups rows having the same value.

Example:

Input:

| request_at |
|------------|
| 2013-10-01 |
| 2013-10-01 |
| 2013-10-02 |
| 2013-10-02 |
| 2013-10-03 |

After:

```sql
GROUP BY request_at
```

Groups become:

```
Group 1
---------
2013-10-01
2013-10-01

Group 2
---------
2013-10-02
2013-10-02

Group 3
---------
2013-10-03
```

Now aggregate functions like

- COUNT()
- SUM()
- AVG()
- MAX()
- MIN()

operate **on each group**.

---

# HAVING

`HAVING` is executed **after `GROUP BY`**.

It filters **groups**, not individual rows.

### Execution

```
Rows
   │
   ▼
GROUP BY
   │
   ▼
Groups
   │
   ▼
HAVING (Filter groups)
```

---

## HAVING is mainly meant for aggregate conditions.

Examples:

```sql
HAVING COUNT(*) > 5
```

```sql
HAVING SUM(amount) > 1000
```

```sql
HAVING AVG(price) >= 500
```

```sql
HAVING MAX(salary) > 100000
```

---

## Correct Example

```sql
SELECT request_at,
       COUNT(*) AS total
FROM Trips
GROUP BY request_at
HAVING COUNT(*) >= 2;
```

Output:

| request_at | total |
|------------|-------|
|2013-10-01|3|
|2013-10-03|2|

Here, `HAVING` checks **each group** after grouping.

---

# Incorrect Usage

```sql
SELECT request_at,
       COUNT(*)
FROM Trips
GROUP BY request_at
HAVING banned = 'No';
```

❌ Wrong

Reason:

After grouping, SQL no longer works with individual rows.

A group may contain many rows having different values of `banned`.

So SQL doesn't know **which row's `banned` value** to compare.

Use `WHERE` instead.

---

# Rule to Remember

## WHERE

- Filters **rows**
- Executes **before GROUP BY**
- Uses normal columns

Example:

```sql
WHERE banned = 'No'
```

---

## HAVING

- Filters **groups**
- Executes **after GROUP BY**
- Usually uses aggregate functions

Example:

```sql
HAVING COUNT(*) > 5
```

---

# Easy Interview Trick

Ask yourself:

> **Am I filtering rows or groups?**

If filtering **rows**

→ Use `WHERE`

If filtering **groups**

→ Use `HAVING`

---

# Summary

| Clause | Works On | Executed | Common Usage |
|---------|----------|----------|--------------|
| WHERE | Individual Rows | Before GROUP BY | `WHERE age > 20` |
| GROUP BY | Creates Groups | After WHERE | `GROUP BY department` |
| HAVING | Groups | After GROUP BY | `HAVING COUNT(*) > 5` |

---

# One-Line Memory Trick

> **WHERE filters rows. GROUP BY creates groups. HAVING filters groups.**