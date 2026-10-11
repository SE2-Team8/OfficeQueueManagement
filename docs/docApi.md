# Office Queue Management API

This document describes the HTTP API exposed by the server in its current state. The backend is implemented with FastAPI and is organized by feature.

## Base URL

When started with the project default configuration, the server is available at:

```text
http://localhost:8000
```

The app exposes UI at:

```text
http://localhost:8000/docs
```

---

## 1. Available services

### Endpoint

```http
GET /tickets/services
```

### Description

Returns the list of published services currently available in the queue system.

### Response

- Status: `200 OK`
- Content type: `application/json`

### Response schema

```json
[
  {
    "tag_name": "SHIPPING",
    "service_time": 10
  },
  {
    "tag_name": "ACCOUNTS",
    "service_time": 15
  },
  {
    "tag_name": "DEPOSIT",
    "service_time": 5
  }
]
```

### Fields

| Field | Type | Description |
| --- | --- | --- |
| `tag_name` | string | Service label used in the queue system |
| `service_time` | integer | Estimated waiting time in minutes for that service |

### Example response

```json
[
  {
    "tag_name": "SHIPPING",
    "service_time": 10
  },
  {
    "tag_name": "ACCOUNTS",
    "service_time": 15
  },
  {
    "tag_name": "DEPOSIT",
    "service_time": 5
  }
]
```

---

## 2. Create a ticket

### Endpoint

```http
POST /tickets/
```

### Description

Creates a new ticket for the selected service. The ticket is added to the in-memory queue for that service.

### Request body

```json
{
  "service_tag": "SHIPPING"
}
```

### Request schema

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `service_tag` | string | Yes | The service tag to request. The accepted values are `SHIPPING`, `ACCOUNTS`, and `DEPOSIT` |

### Response

- Status: `200 OK`
- Content type: `application/json`

### Response schema

```json
{
  "id": 1,
  "code": "S1",
  "service_type": "SHIPPING",
  "issued_at": "2026-10-09T07:43:42.213000Z",
  "status": "WAITING"
}
```

### Fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | integer | Sequential ticket number for the selected service |
| `code` | string | Ticket code composed from the service code and counter, for example `S1`, `A2`, `D3` |
| `service_type` | string | Service requested by the customer |
| `issued_at` | datetime | Ticket issuance timestamp in UTC |
| `status` | string | Current status; initially `WAITING` and later updated to `CALLED` when picked by a counter |

### Example request

```http
POST /tickets/
Content-Type: application/json

{
  "service_tag": "ACCOUNTS"
}
```

### Example response

```json
{
  "id": 2,
  "code": "A2",
  "service_type": "ACCOUNTS",
  "issued_at": "2026-10-09T07:45:10.000000Z",
  "status": "WAITING"
}
```

### Error responses

#### Service not found

```http
404 Not Found
```

```json
{
  "detail": "Service not found"
}
```

This occurs when `service_tag` does not match one of the configured services.

---

## 3. Display a ticket page

### Endpoint

```http
GET /tickets/{ticket_code}
```

### Description

Returns an HTML page that displays the requested ticket code in a simplified card layout. This is used to show the customer their generated ticket.

### Path parameter

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `ticket_code` | string | Yes | Code of the ticket to display, such as `S1` or `A2` |

### Response

- Status: `200 OK`
- Content type: `text/html`

### Example

```http
GET /tickets/S1
```

The endpoint returns an HTML page similar to:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Ticket S1</title>
  </head>
  <body>
    <div class="card">
      <p class="label">Your ticket is</p>
      <div class="code">S1</div>
    </div>
  </body>
</html>
```

The ticket code is escaped before rendering to reduce HTML injection risk.

---

## 4. List counters

### Endpoint

```http
GET /counters/
```

### Description

Returns the list of counters configured in the office.

### Response

- Status: `200 OK`
- Content type: `application/json`

### Response schema

```json
[
  {
    "id": 1,
    "services": ["SHIPPING", "ACCOUNTS", "DEPOSIT"]
  },
  {
    "id": 2,
    "services": ["SHIPPING", "ACCOUNTS", "DEPOSIT"]
  },
  {
    "id": 3,
    "services": ["SHIPPING", "ACCOUNTS", "DEPOSIT"]
  }
]
```

### Fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | integer | Identifier of the counter |
| `services` | array of strings | Services managed by the counter |

### Example response

```json
[
  {
    "id": 1,
    "services": ["SHIPPING", "ACCOUNTS", "DEPOSIT"]
  }
]
```

---

## 5. Call the next customer

### Endpoint

```http
POST /counters/{counter_id}/next
```

### Description

Returns the next customer waiting in the queues handled by the specified counter. The API selects the candidate queue with the largest number of pending customers; if there is a tie, it prioritizes the service with the shortest estimated service time.

### Path parameter

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `counter_id` | integer | Yes | Counter identifier |

### Response when a customer is available

- Status: `200 OK`
- Content type: `application/json`

### Response schema

```json
{
  "ticket_code": "S2",
  "service_type": "SHIPPING",
  "counter_id": 1,
  "queue_length": 2
}
```

### Fields

| Field | Type | Description |
| --- | --- | --- |
| `ticket_code` | string | Code of the next ticket assigned to the counter |
| `service_type` | string | Service category served by that ticket |
| `counter_id` | integer | Counter from which the customer was called |
| `queue_length` | integer | Number of remaining tickets in that service queue |

### Example response

```json
{
  "ticket_code": "A3",
  "service_type": "ACCOUNTS",
  "counter_id": 2,
  "queue_length": 1
}
```

### Response when no customer is waiting

- Status: `204 No Content`

This case is returned when the selected counter has no pending tickets in any of the services it manages.

### Error responses

#### Counter not found

```http
404 Not Found
```

```json
{
  "detail": "Counter not found"
}
```

