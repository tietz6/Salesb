# Telegram Modules & DeepSeek Integration - Quick Start Guide

## 🎯 Overview

This guide covers the complete Telegram integration and DeepSeek AI functionality for the Salesbot "На Счастье" project.

## 📦 What's Included

### 1. Telegram Bot Integration (`integrations/telegram_bot/v1`)
- Webhook-based Telegram bot
- AI-powered responses via DeepSeek
- Brand-consistent communication

### 2. Telegram Push Notifications (`integrations/telegram_push/v1`)
- Multi-channel notification system
- Event-based triggers
- Template-based messaging

### 3. DeepSeek Persona (`modules/deepseek_persona/v1`)
- Brand voice configuration
- Role-based response styling
- Template management

### 4. Voice Gateway (`core/voice_gateway/v1`)
- Core DeepSeek API integration
- LLM chat interface
- Automatic fallback mode

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd "Бот/salesbot_final(копия)"
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create a `.env` file or set environment variables:

```bash
# Telegram Bot Token (required)
export TELEGRAM_BOT_TOKEN="8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI"

# DeepSeek API (required for AI features)
export DEEPSEEK_API_KEY="sk-4de54b0041b44cf193b22cf21f028be7"
export DEEPSEEK_MODEL="deepseek-chat"
export DEEPSEEK_API_URL="https://api.deepseek.com/v1/chat/completions"

# Optional settings
export HTTP_TIMEOUT=15
export HTTP_RETRIES=2
export TELEGRAM_PUSH_MOCK_MODE=false
```

### Step 3: Start the Application

```bash
# Start the main API server
python main.py
# or
python -m uvicorn startup:app --host 0.0.0.0 --port 8080 --reload
```

### Step 4: Start the Telegram Bot

Option A - Using simple_telegram_bot.py (Polling):
```bash
python simple_telegram_bot.py
```

Option B - Using telegram_bot.py with webhook (requires setup):
```bash
# First, configure webhook
curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=https://your-domain.com/telegram_bot/v1/webhook"

# Then start the bot
python telegram_bot.py
```

## 🔧 Configuration Files

### DeepSeek Persona Configuration
Location: `modules/deepseek_persona/v1/data/persona.json`

Contains:
- Brand identity ("На Счастье")
- Communication rules
- Role templates (coach, client_emotional, client_rational)
- Opening phrases

### Telegram Push Templates
Location: `integrations/telegram_push/v1/data/push_formats.json`

Contains message templates for:
- Training reminders
- KPI updates
- Deal notifications
- Case assignments

### Telegram Push Configuration
Location: `integrations/telegram_push/v1/data/config.json`

Settings:
```json
{
  "enabled": true,
  "mock_mode": false,
  "bot_token_env": "TELEGRAM_BOT_TOKEN"
}
```

## 📱 Using the Telegram Bot

### Basic Commands

1. **Start conversation**
   ```
   /start
   ```
   Bot shows welcome message

2. **Ask questions**
   ```
   Как создать песню для жены?
   ```
   Bot responds using DeepSeek AI with brand persona

3. **Training mode** (via simple_telegram_bot.py)
   ```
   /train
   ```
   Starts training dialog simulation

### Webhook Mode vs Polling Mode

**Polling Mode** (simple_telegram_bot.py):
- ✅ Easy to set up
- ✅ Works behind firewall
- ✅ Good for development
- ❌ Less efficient

**Webhook Mode** (telegram_bot.py):
- ✅ More efficient
- ✅ Real-time updates
- ✅ Production-ready
- ❌ Requires public URL
- ❌ SSL certificate needed

## 🎨 Using DeepSeek Persona

### In Code

```python
from modules.deepseek_persona.v1.service import persona_chat, apply_persona

# Generate AI response with brand voice
response = persona_chat(
    "Клиент спрашивает о цене",
    role="coach"
)

# Apply brand style to text
styled = apply_persona(
    role="client_emotional",
    text="Хочу песню для мамы"
)
```

### Via API

```bash
# Chat endpoint
curl -X POST http://localhost:8080/deepseek_persona/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Как начать разговор с клиентом?",
    "role": "coach"
  }'

# Stylize endpoint
curl -X POST http://localhost:8080/deepseek_persona/v1/stylize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Расскажите о вашем бюджете",
    "role": "coach"
  }'
```

## 📢 Using Push Notifications

### Subscribe Manager

```bash
curl -X POST http://localhost:8080/telegram_push/v1/subscribe \
  -H "Content-Type: application/json" \
  -d '{
    "manager_id": "alex",
    "chat_id": "123456789",
    "channels": ["training", "kpi", "deals", "cases"]
  }'
```

### Send Notifications

```bash
# Training reminder
curl -X POST http://localhost:8080/telegram_push/v1/events/training_reminder \
  -H "Content-Type: application/json" \
  -d '{
    "manager_id": "alex",
    "when": "сегодня в 14:00",
    "mode": "Arena"
  }'

# KPI update
curl -X POST http://localhost:8080/telegram_push/v1/events/percent_up \
  -H "Content-Type: application/json" \
  -d '{
    "manager_id": "alex",
    "percent": 15.0
  }'

# Deal won
curl -X POST http://localhost:8080/telegram_push/v1/events/deal_won \
  -H "Content-Type: application/json" \
  -d '{
    "manager_id": "alex",
    "id": "L-1001",
    "amount": 12000,
    "income": 2400
  }'
```

## 🧪 Testing

### Test DeepSeek Integration

```python
from core.voice_gateway.v1 import VoicePipeline

vp = VoicePipeline()
messages = [
    {"role": "system", "content": "Ты коуч по продажам"},
    {"role": "user", "content": "Как улучшить продажи?"}
]
response = vp.llm.chat(messages)
print(f"Response: {response}")
```

### Test Telegram Bot (Health Check)

```bash
curl http://localhost:8080/telegram_bot/v1/health
# Should return: {"ok": true}
```

### Test Push Notifications (Mock Mode)

```bash
# Check current mode
curl http://localhost:8080/telegram_push/v1/health

# View logs
curl http://localhost:8080/telegram_push/v1/log
```

## 🔍 Troubleshooting

### Bot Not Responding

1. Check bot token:
   ```bash
   echo $TELEGRAM_BOT_TOKEN
   ```

2. Verify webhook (if using webhook mode):
   ```bash
   curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo"
   ```

3. Check logs:
   ```bash
   # Application logs
   tail -f logs/app.log
   ```

### DeepSeek API Issues

1. Verify API key:
   ```bash
   echo $DEEPSEEK_API_KEY
   ```

2. Test connection:
   ```bash
   curl -X POST https://api.deepseek.com/v1/chat/completions \
     -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "deepseek-chat",
       "messages": [{"role": "user", "content": "Hello"}]
     }'
   ```

3. Check fallback mode:
   - If API unavailable, system uses local mode
   - Look for "локальный режим" in responses

### Push Notifications Not Sending

1. Check mock mode:
   ```bash
   # Edit data/config.json
   {
     "mock_mode": false  # Set to false for real sending
   }
   ```

2. Verify subscription:
   ```bash
   curl http://localhost:8080/telegram_push/v1/subscribers
   ```

3. Check token:
   ```bash
   echo $TELEGRAM_BOT_TOKEN
   ```

## 📚 Additional Documentation

- **Telegram Bot**: See `integrations/telegram_bot/README.md`
- **Push Notifications**: See `integrations/telegram_push/README.md`
- **DeepSeek Persona**: See `modules/deepseek_persona/README.md`
- **Voice Gateway**: See `core/voice_gateway/v1/README.md`

## 🔐 Security Notes

### API Keys
- Never commit API keys to git
- Use environment variables
- Rotate keys regularly

### Webhook Security
- Use HTTPS only
- Verify Telegram webhook signature (recommended)
- Implement rate limiting

### Data Privacy
- DeepSeek processes messages externally
- Don't send sensitive personal data
- Consider data anonymization

## 🚦 Production Checklist

- [ ] Set `DEEPSEEK_API_KEY` in production environment
- [ ] Set `TELEGRAM_BOT_TOKEN` in production environment
- [ ] Configure webhook with HTTPS URL
- [ ] Set `TELEGRAM_PUSH_MOCK_MODE=false` for real notifications
- [ ] Set up monitoring for API errors
- [ ] Configure rate limiting
- [ ] Set up log rotation
- [ ] Test fallback mode
- [ ] Verify all integrations work
- [ ] Document custom configurations

## 🆘 Support

If you encounter issues:

1. Check the detailed README files in each module
2. Review error logs
3. Test with minimal configuration
4. Verify all environment variables are set
5. Check DeepSeek API status and quotas

## 🎉 Success!

Your Telegram integration with DeepSeek AI is now complete and ready to use!

The system includes:
✅ Telegram bot with AI responses
✅ Push notification system
✅ Brand-consistent communication
✅ Graceful fallback handling
✅ Comprehensive documentation
✅ Production-ready code
