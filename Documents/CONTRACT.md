# Contract – Voice Help Desk Agent

---

# 1. Room Naming Convention

Room names will follow the format:

```
helpdesk-{room-id}
```

Example:

```
helpdesk-a1b2c3d4
```

---

# 2. Token Endpoint

## Endpoint

```
POST /api/token
```

## Request

```json
{
  "user_name": "John Doe"
}
```

## Response

```json
{
  "token": "<JWT_TOKEN>",
  "room_name": "helpdesk-a1b2c3d4",
  "identity": "John Doe"
}
```

---

# 3. RPC Notification Payload

The agent sends an RPC notification to the frontend after a successful account unlock.

```json
{
  "event": "account_unblocked",
  "username": "jdoe",
  "message": "Account jdoe has been unblocked."
}
```

| Field | Type | Description |
|--------|------|-------------|
| event | string | Notification event name |
| username | string | Username of the affected account |
| message | string | Message displayed in the frontend |

---

# 4. SQLite User Schema

**Table:** `users`

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| username | TEXT | UNIQUE NOT NULL |
| full_name | TEXT | NOT NULL |
| email | TEXT | UNIQUE NOT NULL |
| status | TEXT | NOT NULL |
| created_at | TEXT | DEFAULT CURRENT_TIMESTAMP |

---

# 5. User Status Values

The following account statuses are supported:

- Active
- Locked
- Disabled