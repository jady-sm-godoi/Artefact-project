# Data Model: CLI Question-Answer Agent with Calculator

## Entities

### Session

A single conversation from agent start to exit. Maintains context for
follow-up questions.

| Field | Type | Description |
|-------|------|-------------|
| conversation_id | UUID | Unique identifier for the session |
| messages | list[Message] | Ordered list of exchanged messages |
| created_at | datetime | Session start timestamp |
| verbose | bool | Whether `--verbose` mode is active |

### Message

A single exchange in the conversation.

| Field | Type | Description |
|-------|------|-------------|
| role | enum (user, assistant, tool) | Who sent the message |
| content | str | The message text or tool result |
| tool_calls | list[ToolCall] | Tool invocations (if any), only in verbose mode |
| timestamp | datetime | When the message was exchanged |

### ToolCall

Record of a calculator tool invocation (verbose mode only).

| Field | Type | Description |
|-------|------|-------------|
| tool_name | str | Name of the tool invoked (e.g., "calculator") |
| input | str | The expression passed to the tool |
| output | str | The result returned by the tool |
| duration_ms | int | How long the tool took to execute |

## State Transitions

```
[Start] → AwaitingInput → Processing → AwaitingInput → ... → [Exit]
                ↑              |
                └── (error) ───┘
```

- **Start**: Agent initializes, shows prompt
- **AwaitingInput**: Idle, waiting for user to type
- **Processing**: Agent is generating a response (knowledge or tool call)
- **Exit**: User typed "exit" or "quit"
