# Voice Gateway v1 - DeepSeek AI Integration

## Overview
Core gateway for AI-powered voice and chat capabilities. Provides unified interface to DeepSeek LLM, ASR (speech recognition), and TTS (text-to-speech) services.

## Architecture

```
VoicePipeline
├── llm (LLMClient) - DeepSeek chat completions
├── asr (ASRStub) - Speech-to-text (stub implementation)
└── tts (TTSStub) - Text-to-speech (stub implementation)
```

## DeepSeek Integration

### LLMClient

The `_LLMClient` class provides OpenAI-compatible interface to DeepSeek API with:
- Automatic retry mechanism
- Role normalization (system/user/assistant/tool)
- Graceful fallback to local mode
- Support for multiple HTTP clients

### Configuration

Environment variables:
```bash
# Required for DeepSeek API
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx

# Optional (has defaults)
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
DEEPSEEK_MODEL=deepseek-chat
HTTP_TIMEOUT=15
HTTP_RETRIES=2
```

### Basic Usage

```python
from core.voice_gateway.v1 import VoicePipeline

# Create pipeline instance
vp = VoicePipeline()

# Chat with DeepSeek
messages = [
    {"role": "system", "content": "Ты помощник проекта 'На Счастье'"},
    {"role": "user", "content": "Как начать разговор с клиентом?"}
]

response = vp.llm.chat(messages)
print(response)
```

## Message Format

### Supported Roles

DeepSeek accepts these roles:
- `system` - System instructions/context
- `user` - User messages
- `assistant` - AI responses (for history)
- `tool` - Tool/function call results

### Role Normalization

The client automatically normalizes custom roles:

```python
messages = [
    {"role": "coach", "content": "..."},      # → converted to "user"
    {"role": "boss", "content": "..."},       # → converted to "system"
    {"role": "client_emotional", "content": "..."}  # → converted to "user"
]

response = vp.llm.chat(messages)  # Works seamlessly
```

## API Response Formats

DeepSeek returns responses in two possible formats:

### Format 1: Simple Output
```json
{
  "output": "Generated text response"
}
```

### Format 2: OpenAI-Compatible
```json
{
  "choices": [
    {
      "message": {
        "content": "Generated text response"
      }
    }
  ]
}
```

The client handles both formats automatically.

## Local Fallback Mode

When DeepSeek API is unavailable (no key, network issues, quota exceeded), the system automatically falls back to local coach mode:

### Fallback Features
- Analyzes message content for common patterns
- Provides context-appropriate advice
- Maintains conversation flow
- Never throws errors

### Example Fallback Responses

For price objection:
```
"Совет коуча: переведи разговор к ценности результата 
и разложи стоимость на шаги/части."
```

For short message:
```
"Совет коуча: расширь ответ ещё 1–2 фразами, 
чтобы создать больше доверия."
```

For missing questions:
```
"Совет коуча: добавь 1–2 уточняющих вопроса, 
чтобы лучше понять человека."
```

## HTTP Client Support

The module tries to use HTTP clients in this order:

1. **integrations.patch_v4.http_client** (preferred)
2. **integrations.patch_v3.http_client** (fallback)
3. **requests library** (last resort)

This ensures compatibility across different project configurations.

## Error Handling

### Network Errors
- Automatic retry with exponential backoff
- Configurable retry count (HTTP_RETRIES)
- Graceful degradation to local mode

### Timeout Handling
- Configurable timeout (HTTP_TIMEOUT)
- Returns local advice if API times out

### Invalid Responses
- Parses both response formats
- Returns local fallback if response unparseable

## ASR & TTS (Future Enhancement)

Currently stub implementations:

### ASR (Automatic Speech Recognition)
```python
audio_bytes = b"..."  # Audio file bytes
text = vp.asr.transcribe(audio_bytes, lang="ru")
# Currently returns: "[asr-stub] распознавание недоступно в офлайн-режиме"
```

### TTS (Text-to-Speech)
```python
text = "Привет!"
audio = vp.tts.synth(text, voice="neutral")
# Currently returns: b"[tts-stub]"
```

These can be replaced with real implementations (AssemblyAI, pyttsx3, etc.) without changing the interface.

## Integration Examples

### Training Coach
```python
from core.voice_gateway.v1 import VoicePipeline

vp = VoicePipeline()

# Generate coach feedback
messages = [
    {"role": "system", "content": "Ты коуч по продажам"},
    {"role": "user", "content": "Менеджер сказал: 'Ну, подумайте...'"}
]

advice = vp.llm.chat(messages)
# Returns coach feedback on how to improve
```

### Client Simulation
```python
# Simulate emotional client response
messages = [
    {"role": "system", "content": "Ты клиент проекта 'На Счастье', эмоциональный тип"},
    {"role": "user", "content": "Менеджер: Расскажите, кому дарите песню?"}
]

client_reply = vp.llm.chat(messages)
# Returns realistic client response
```

### Objection Handling
```python
# Generate response to objection
messages = [
    {"role": "system", "content": "Ты эксперт по работе с возражениями"},
    {"role": "user", "content": "Клиент: Это слишком дорого"}
]

suggestion = vp.llm.chat(messages)
# Returns advice on handling price objection
```

## Performance Considerations

### Timeout Settings
- Default: 15 seconds
- Recommendation: 10-20 seconds for chat
- Increase for complex prompts

### Retry Strategy
- Default: 2 retries
- 0.25 second delay between retries
- Exponential backoff recommended for production

### Rate Limiting
DeepSeek API has rate limits:
- Monitor `429 Too Many Requests` responses
- Implement request queuing if needed
- Consider caching for repeated queries

## Testing

### Test LLM Connection
```python
from core.voice_gateway.v1 import VoicePipeline

vp = VoicePipeline()
response = vp.llm.chat([
    {"role": "user", "content": "Привет, это тест"}
])
print(f"Response: {response}")
```

### Test Fallback Mode
```python
import os
# Temporarily remove API key
old_key = os.environ.get('DEEPSEEK_API_KEY')
os.environ.pop('DEEPSEEK_API_KEY', None)

vp = VoicePipeline()
response = vp.llm.chat([
    {"role": "user", "content": "Цена слишком высокая"}
])
# Should return local coach advice

# Restore key
if old_key:
    os.environ['DEEPSEEK_API_KEY'] = old_key
```

## Security

### API Key Storage
- Never commit API keys to git
- Use environment variables
- Consider secrets management service

### Data Privacy
- DeepSeek API processes messages externally
- Don't send sensitive personal data
- Implement data anonymization if needed

## Troubleshooting

### "No API key" Error
```
Solution: Set DEEPSEEK_API_KEY environment variable
```

### Timeout Issues
```
Solution: Increase HTTP_TIMEOUT (e.g., to 30)
```

### "Unexpected response" Errors
```
Solution: Check DEEPSEEK_API_URL is correct
Verify API key has access to model
```

### Local Fallback Activating
```
Check: API key is set correctly
Check: Network connectivity to api.deepseek.com
Check: API quota not exceeded
```

## Related Modules

- `modules/deepseek_persona/` - Brand-specific persona configuration
- `integrations/telegram_bot/v1/` - Uses VoicePipeline for bot responses
- `modules/trainer_*/` - Training modules using LLM for feedback
- `modules/arena/` - Client simulation using LLM

## Future Enhancements

1. **Real ASR Integration**
   - AssemblyAI for speech recognition
   - Multiple language support
   - Real-time transcription

2. **Real TTS Integration**
   - pyttsx3 for offline synthesis
   - Cloud TTS services
   - Voice cloning capabilities

3. **Streaming Support**
   - Real-time response streaming
   - Better UX for long responses

4. **Caching Layer**
   - Cache common queries
   - Reduce API costs
   - Improve response times

5. **Advanced Error Handling**
   - Circuit breaker pattern
   - Request queuing
   - Priority-based processing
