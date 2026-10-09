# Ticket API Documentation

This document describes the ticket-related endpoints exposed by the application under the `/tickets` route.

## Base path

```text
/tickets
```

## 1. Get available services

### Endpoint

```http
GET /tickets/services
```

### Description

Returns the list of services currently available in the queue system.

### Response

- Status: `200 OK`
- Content type: `application/json`

### Response schema

```json
[
  {
    "tag_name": "SHIPPING",
    "service_time": 10
  }
]
```

### Fields

| Field | Type | Description |
| --- | --- | --- |
| `tag_name` | string | Service identifier/tag |
| `service_time` | integer | Estimated waiting time in minutes |

### Example response

```json
[
  {
    "tag_name": "SHIPPING",
    "service_time": 10
  },
  {
    "tag_name": "ACCOUNTS",
    "service_time": 10
  },
  {
    "tag_name": "DEPOSIT",
    "service_time": 10
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

Creates a new ticket for the selected service.

### Request body

```json
{
  "service_tag": "SHIPPING"
}
```

### Request schema

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `service_tag` | string | Yes | Service tag to request a ticket for |

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
| `id` | integer | Sequential ticket identifier for the selected service |
| `code` | string | Ticket code, composed from the service code and its counter (for example `S1`, `A2`, `D3`) |
| `service_type` | string | The requested service tag |
| `issued_at` | datetime | Ticket creation timestamp |
| `status` | string | Current ticket status; currently always `WAITING` |

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

This error is returned when the `service_tag` does not match any available service.

---

## 3. Display a ticket page

### Endpoint

```http
GET /tickets/{ticket_code}
```

### Description

Returns an HTML page showing the requested ticket code in a stylized card layout.

### Path parameter

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `ticket_code` | string | Yes | Ticket code to display, such as `S1` |

### Response

- Status: `200 OK`
- Content type: `text/html`

### Example

```http
GET /tickets/S1
```

This returns a page similar to:

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

The value is escaped before being rendered to reduce the risk of HTML injection in the displayed ticket code.

---
