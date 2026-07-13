# Joining the Same Table Multiple Times (Self Join with Aliases)

Sometimes a table contains **multiple foreign keys** that reference the **same table**.

## Example

### Trips Table

| id | client_id | driver_id |
|----|-----------|-----------|
| 1  | 101       | 201       |

### Users Table

| users_id | name |
|----------|------|
| 101      | Alice |
| 201      | Bob |

Here,

- `client_id` → references `Users.users_id`
- `driver_id` → also references `Users.users_id`

Both foreign keys point to the **Users** table.

---

## ❌ Incorrect Query

```sql
SELECT *
FROM Trips t
JOIN Users u
ON t.client_id = u.users_id
AND t.driver_id = u.users_id;
```

### Why is it wrong?

The condition becomes:

```text
t.client_id = u.users_id
AND
t.driver_id = u.users_id
```

This means the **same user** must be both the client and the driver.

Example:

```text
client_id = 101
driver_id = 201
```

Checking `users_id = 101`

```text
101 = 101 ✅
201 = 101 ❌
```

Checking `users_id = 201`

```text
101 = 201 ❌
201 = 201 ✅
```

No row matches.

This query only works if:

```text
client_id = driver_id
```

which is usually **not true**.

---

## ✅ Correct Query

Use **two joins** with **different aliases**.

```sql
SELECT *
FROM Trips t
JOIN Users c
ON t.client_id = c.users_id
JOIN Users d
ON t.driver_id = d.users_id;
```

Where:

- `c` → Client
- `d` → Driver

Now each foreign key is matched with its own row in the `Users` table.

---

## Visualization

```
            Users
          +--------+
          |users_id|
          +--------+
             ^    ^
             |    |
   client_id |    | driver_id
             |    |
          +------------+
          |   Trips    |
          +------------+
```

Since **two foreign keys point to the same table**, we need **two aliases**.

---

## Rule to Remember

> **If multiple foreign keys reference the same table, join that table once for each foreign key using different aliases.**

Example:

```sql
JOIN Users client
ON Trips.client_id = client.users_id

JOIN Users driver
ON Trips.driver_id = driver.users_id
```

---

# Quick Interview Tip

Whenever you see:

- `manager_id`
- `employee_id`
- `client_id`
- `driver_id`
- `sender_id`
- `receiver_id`

all pointing to the same table,

👉 **Use multiple joins with different aliases.**