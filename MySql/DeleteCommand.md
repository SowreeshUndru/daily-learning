# MySQL Self JOIN and Primary Key Constraints

## Query

```sql
DELETE p1
FROM Person p1
JOIN Person p2
ON p1.email = p2.email
AND p1.id > p2.id;
```

---

# Why doesn't the Primary Key constraint cause an error here?

The answer is **because this query is only reading the data to determine which rows should be deleted.**

The `JOIN` operation does **not** modify the table. It simply creates a temporary result set by comparing rows.

Primary key constraints are **not checked while reading data**.

---

# Golden Rule: When Constraints Are Checked

## 1. Constraints Trigger During Writes ✅

Whenever you execute:

* `INSERT`
* `UPDATE`

MySQL validates the constraints.

For a **PRIMARY KEY**, MySQL checks that:

* The value is **unique**
* The value is **NOT NULL**

Example:

```sql
INSERT INTO Person(id, email)
VALUES (1, 'abc@gmail.com');
```

If `id = 1` already exists, MySQL throws an error because the Primary Key constraint is violated.

Think of the Primary Key constraint as a **security guard at the entrance**. Whenever new data enters or existing data changes, it verifies that the rules are followed.

---

## 2. Constraints Do Nothing During Reads ✅

Whenever you execute:

* `SELECT`
* `JOIN`
* `GROUP BY`
* `ORDER BY`
* Aggregate functions (`COUNT`, `SUM`, `AVG`, etc.)

MySQL is only reading data that already exists.

Since no data is being inserted or updated, **Primary Key constraints are not checked.**

Example:

```sql
SELECT *
FROM Person p1
JOIN Person p2
ON p1.email = p2.email;
```

Even though the same row may appear multiple times in the result, this is perfectly valid because the database is only displaying data—it is **not changing it**.

---

# Accessing Columns After a JOIN

After assigning aliases to tables, you can access columns using the alias.

For example:

```sql
SELECT p1.*
FROM Person p1
JOIN Person p2
ON p1.email = p2.email;
```

Returns **all columns** from `p1`.

You can also access individual columns:

```sql
SELECT
    p1.id,
    p1.email,
    p2.id,
    p2.email
FROM Person p1
JOIN Person p2
ON p1.email = p2.email;
```

Or mix them:

```sql
SELECT
    p1.*,
    p2.email
FROM Person p1
JOIN Person p2
ON p1.email = p2.email;
```

The aliases (`p1`, `p2`) simply tell MySQL **which copy of the table** a column belongs to.

---

# Why Do We Write `DELETE p1`?

When using a JOIN, there may be multiple tables (or multiple aliases of the same table).

```sql
DELETE p1
FROM Person p1
JOIN Person p2
ON ...
```

Here:

* `p1` → Rows that will be deleted.
* `p2` → Used only for comparison.

If you wrote:

```sql
DELETE p2
```

then MySQL would delete rows represented by `p2` instead.

---

# Why Is `AND p1.id > p2.id` Necessary?

Suppose the table contains:

| id | email                             |
| -- | --------------------------------- |
| 1  | [a@gmail.com](mailto:a@gmail.com) |
| 2  | [a@gmail.com](mailto:a@gmail.com) |
| 3  | [b@gmail.com](mailto:b@gmail.com) |

If the query is:

```sql
SELECT *
FROM Person p1
JOIN Person p2
ON p1.email = p2.email;
```

The JOIN result is:

| p1.id | p2.id |
| ----- | ----- |
| 1     | 1     |
| 1     | 2     |
| 2     | 1     |
| 2     | 2     |
| 3     | 3     |

Notice that every row joins with itself.

Adding

```sql
AND p1.id > p2.id
```

filters the result to:

| p1.id | p2.id |
| ----- | ----- |
| 2     | 1     |

Now only the duplicate row (the one with the larger `id`) is selected for deletion.

---

# Final Query

```sql
DELETE p1
FROM Person p1
JOIN Person p2
ON p1.email = p2.email
AND p1.id > p2.id;
```

This query:

1. Finds rows having the same email.
2. Keeps the row with the smallest `id`.
3. Deletes rows with larger `id`s.

---

