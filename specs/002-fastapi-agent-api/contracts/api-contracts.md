# API Contract: Query Endpoint

## POST /query

Submit a question or calculation to the agent.

### Request

```
Content-Type: application/json
```

```json
{
  "query": "What is the capital of France?",
  "session_id": "optional-uuid-string",
  "verbose": false
}
```

### Response: 200 OK

```json
{
  "response": "Paris",
  "tool_calls": null
}
```

### Response: 200 OK (verbose)

```json
{
  "response": "5888",
  "tool_calls": [
    {
      "tool_name": "calculator",
      "input": "128 * 46",
      "output": "5888",
      "duration_ms": 12
    }
  ]
}
```

### Response: 422 Validation Error

```json
{
  "detail": "field required: query"
}
```

### Response: 504 Gateway Timeout

```json
{
  "detail": "Agent response exceeded 30 seconds"
}
```

---

# API Contract: Health Endpoint

## GET /health

Check API status.

### Response: 200 OK (normal)

```json
{
  "status": "ok",
  "mode": "full"
}
```

### Response: 200 OK (degraded)

```json
{
  "status": "degraded",
  "mode": "calculator-only"
}
```
