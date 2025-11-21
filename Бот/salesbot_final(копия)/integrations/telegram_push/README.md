# Telegram Push Notifications (v1)

## Overview
Push notification system for sending targeted messages to managers via Telegram. Supports multiple channels, event-based triggers, and template-based messaging.

## Features
- Multi-channel subscription system (training, kpi, cases, deals)
- Template-based message formatting
- Mock mode for testing without sending real messages
- Event hooks for common scenarios
- Message logging (JSONL format)

## API Endpoints

### GET /telegram_push/v1/health
Health check endpoint.

### GET /telegram_push/v1/subscribers
Get all subscriber data.

### POST /telegram_push/v1/subscribe
Subscribe a manager to notification channels.

**Body:**
```json
{
  "manager_id": "alex",
  "chat_id": "123456789",
  "channels": ["training", "kpi", "deals", "cases"]
}
```

### POST /telegram_push/v1/send
Send a custom push notification.

**Body:**
```json
{
  "manager_id": "alex",
  "channel": "training",
  "template": "training.reminder",
  "payload": {
    "when": "сегодня",
    "mode": "Arena"
  }
}
```

### Event Endpoints

#### POST /telegram_push/v1/events/training_reminder
Send training reminder.

**Body:**
```json
{
  "manager_id": "alex",
  "when": "сегодня в 11:00",
  "mode": "Arena"
}
```

#### POST /telegram_push/v1/events/percent_up
Notify about performance percentage increase.

**Body:**
```json
{
  "manager_id": "alex",
  "percent": 15.0
}
```

#### POST /telegram_push/v1/events/to_next
Notify about progress to next tier.

**Body:**
```json
{
  "manager_id": "alex",
  "remain": 3,
  "next_percent": "20%"
}
```

#### POST /telegram_push/v1/events/deal_won
Notify about won deal.

**Body:**
```json
{
  "manager_id": "alex",
  "id": "L-1001",
  "amount": 12000,
  "income": 2400
}
```

#### POST /telegram_push/v1/events/deal_lost
Notify about lost deal.

**Body:**
```json
{
  "manager_id": "alex",
  "id": "L-1002"
}
```

### GET /telegram_push/v1/log
Get last 200 push notification log entries.

## Configuration

### Environment Variables
- `TELEGRAM_BOT_TOKEN` or `TG_BOT_TOKEN` - Telegram bot token for sending messages
- `TELEGRAM_PUSH_MOCK_MODE` - Set to "false" to enable real sending (default: true)

### Data Files

#### data/config.json
```json
{
  "enabled": true,
  "mock_mode": true,
  "bot_token_env": "TELEGRAM_BOT_TOKEN"
}
```

#### data/subscribers.json
Stores manager subscriptions:
```json
{
  "alex": {
    "chat_id": "123456789",
    "channels": ["training", "kpi", "deals", "cases"]
  }
}
```

#### data/push_formats.json
Message templates with placeholders:
```json
{
  "training.reminder": "🎯 Напоминание: тренировка {{ when }} в режиме {{ mode }}",
  "kpi.percent_up": "📈 Поздравляем! Ваш процент вырос до {{ percent }}%",
  "deals.won": "🎉 Сделка {{ id }} закрыта! Сумма: {{ amount }}, доход: {{ income }}"
}
```

#### data/send_log.jsonl
Log of all sent/attempted messages (one JSON object per line).

## Channels

- **training** - Training reminders and notifications
- **kpi** - Performance metrics updates
- **cases** - New cases and case updates
- **deals** - Deal status changes (won/lost)

## Mock Mode

In mock mode (default), messages are:
- NOT sent to Telegram
- Written to `send_log.jsonl`
- Returned in API response for testing

To enable real sending:
1. Set `mock_mode: false` in `data/config.json`
2. Or set `TELEGRAM_PUSH_MOCK_MODE=false` environment variable
3. Ensure `TELEGRAM_BOT_TOKEN` is configured

## Template Syntax

Templates use `{{ variable }}` syntax for placeholders:

```
{{ when }} - Time/date
{{ mode }} - Training mode
{{ percent }} - Percentage value
{{ remain }} - Remaining count
{{ next_percent }} - Next tier percentage
{{ id }} - Deal/case ID
{{ amount }} - Amount value
{{ income }} - Income value
```

## Integration Examples

### With Salary Reports
```python
# After calculating new commission
POST /telegram_push/v1/events/percent_up
{
  "manager_id": "alex",
  "percent": 20.0
}
```

### With CRM Bridge
```python
# When deal closes
POST /telegram_push/v1/events/deal_won
{
  "manager_id": "alex",
  "id": "D-1003",
  "amount": 15000,
  "income": 3000
}
```

### With Training Scheduler
```python
# Daily reminder
POST /telegram_push/v1/events/training_reminder
{
  "manager_id": "alex",
  "when": "сегодня в 14:00",
  "mode": "Master Path"
}
```

## Error Handling

- Returns `{"ok": false, "error": "not_subscribed"}` if manager not subscribed
- Returns `{"ok": false, "error": "channel_not_allowed"}` if channel not in subscription
- Returns `{"ok": false, "error": "no_token_env"}` if token not configured (real mode)
- Logs all errors to `send_log.jsonl`

## Testing

1. Subscribe a test user:
```bash
curl -X POST http://localhost:8080/telegram_push/v1/subscribe \
  -H "Content-Type: application/json" \
  -d '{
    "manager_id": "test_user",
    "chat_id": "123456789",
    "channels": ["training", "kpi"]
  }'
```

2. Send test notification:
```bash
curl -X POST http://localhost:8080/telegram_push/v1/events/training_reminder \
  -H "Content-Type: application/json" \
  -d '{
    "manager_id": "test_user",
    "when": "сегодня",
    "mode": "Arena"
  }'
```

3. Check logs:
```bash
curl http://localhost:8080/telegram_push/v1/log
```
