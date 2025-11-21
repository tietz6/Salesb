# Telegram Bot Integration (v1)

## Overview
This module provides Telegram bot integration for the Salesbot application using webhook-based messaging.

## Features
- Webhook endpoint for receiving Telegram updates
- Integration with DeepSeek AI through VoicePipeline
- Brand-styled responses ("На Счастье" persona)
- Health check endpoint

## API Endpoints

### GET /telegram_bot/v1/health
Health check endpoint to verify the module is running.

**Response:**
```json
{
  "ok": true
}
```

### POST /telegram_bot/v1/webhook
Main webhook endpoint for receiving Telegram updates.

**Request body:** Telegram Update object

**Response:**
```json
{
  "ok": true,
  "sent": {
    "ok": true,
    "status": 200,
    "data": {...}
  }
}
```

## Configuration

### Environment Variables
- `TELEGRAM_BOT_TOKEN` or `TG_BOT_TOKEN` - Telegram bot token (required)
- `DEEPSEEK_API_KEY` - DeepSeek API key for AI responses (optional, falls back to local mode)
- `DEEPSEEK_API_URL` - DeepSeek API endpoint (default: https://api.deepseek.com/v1/chat/completions)

## How It Works

1. User sends a message to the Telegram bot
2. Telegram sends update to the webhook endpoint
3. Bot processes the message:
   - `/start` command: Shows welcome message
   - Other text: Sends to DeepSeek AI for response generation
4. Response is styled with brand persona and sent back to user

## DeepSeek Integration

The bot uses `VoicePipeline` from `core.voice_gateway.v1` which provides:
- LLM chat interface (DeepSeek-compatible)
- Automatic fallback to local mode if API is unavailable
- Branded, warm communication style

## Setup

1. Set environment variables:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export DEEPSEEK_API_KEY="your_deepseek_key"
```

2. Configure Telegram webhook:
```bash
curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=https://your-domain.com/telegram_bot/v1/webhook"
```

3. Start the application:
```bash
python main.py
```

## Testing

Test the webhook endpoint:
```bash
curl -X POST http://localhost:8080/telegram_bot/v1/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "chat": {"id": 123456},
      "text": "Привет"
    }
  }'
```

## Error Handling

- If TELEGRAM_BOT_TOKEN is not set, raises RuntimeError on initialization
- If DeepSeek API is unavailable, uses fallback mode with predefined responses
- All exceptions are caught and returned as error responses

## Related Modules

- `core/voice_gateway/v1/pipeline.py` - DeepSeek LLM integration
- `modules/deepseek_persona/` - Brand persona configuration
- `integrations/telegram_push/v1/` - Push notification service
