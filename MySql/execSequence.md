# Execution Order of `LAG()` with `PARTITION BY` and `ORDER BY`

Consider the following query:

```sql
SELECT *,
       LAG(temperature, 1)
       OVER (
           PARTITION BY id
           ORDER BY day
       ) AS prev_temp
FROM weather
ORDER BY temperature;
```

## Execution Order

Think of SQL executing the query like this:

```text
1. FROM weather
        ↓
2. PARTITION BY id
        ↓
3. ORDER BY day (inside OVER, within each partition)
        ↓
4. Compute LAG() for each partition
        ↓
5. SELECT the columns
        ↓
6. ORDER BY temperature (outside OVER, entire result set)
        ↓
7. Return the final output
```

---

## Example Table

| id | day | temp |
|----|-----|------|
| 1 | 1 | 10 |
| 1 | 2 | 20 |
| 1 | 3 | 15 |
| 2 | 1 | 30 |
| 2 | 2 | 25 |

---

## Step 1: Partition by `id`

### Partition 1 (`id = 1`)

| day | temp |
|-----|------|
| 1 | 10 |
| 2 | 20 |
| 3 | 15 |

### Partition 2 (`id = 2`)

| day | temp |
|-----|------|
| 1 | 30 |
| 2 | 25 |

---

## Step 2: Order inside each partition by `day`

### Partition 1

```text
10
20
15
```

### Partition 2

```text
30
25
```

---

## Step 3: Compute `LAG()`

| id | day | temp | prev_temp |
|----|-----|------|-----------|
| 1 | 1 | 10 | NULL |
| 1 | 2 | 20 | 10 |
| 1 | 3 | 15 | 20 |
| 2 | 1 | 30 | NULL |
| 2 | 2 | 25 | 30 |

At this point, **`LAG()` has finished computing its values.**

---

## Step 4: Final `ORDER BY temperature`

Now SQL sorts the **entire result set** by `temperature`.

| id | day | temp | prev_temp |
|----|-----|------|-----------|
| 1 | 1 | 10 | NULL |
| 1 | 3 | 15 | 20 |
| 1 | 2 | 20 | 10 |
| 2 | 2 | 25 | 30 |
| 2 | 1 | 30 | NULL |

### Important

- The `prev_temp` values **do not change**.
- Only the **display order** of the rows changes.

---

# Rule to Remember

- ✅ `PARTITION BY` → Splits the rows into independent groups.
- ✅ `ORDER BY` **inside** `OVER()` → Defines the order within each partition for window functions like `LAG()`, `LEAD()`, `ROW_NUMBER()`, `RANK()`, etc.
- ✅ The window function (`LAG()`) is computed.
- ✅ `ORDER BY` **outside** `OVER()` → Sorts the final result set after all window functions have already been computed.

> **Mental Model:**
>
> `FROM → PARTITION BY → ORDER BY (inside OVER) → Window Function → SELECT → ORDER BY (outside OVER) → Final Output`