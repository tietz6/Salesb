# Salesbot Architecture

## Project Overview

Salesbot is a sales training platform with two main interfaces:
1. **FastAPI REST API** - Web service for accessing training modules
2. **Telegram Bot** - Interactive chat interface for sales training

## Directory Structure

```
salesbot_final(копия)/
├── startup.py                 # FastAPI application entry point
├── main.py                    # Simple uvicorn launcher
├── router_autoload.py         # Automatic route registration for FastAPI
├── telegram_bot.py            # Telegram bot entry point
├── start_core_api.bat         # Windows startup script (both API + Bot)
├── requirements.txt           # Python dependencies
│
├── api/                       # API-specific code
│   ├── core/                  # Telegram bot infrastructure
│   │   ├── registry.py        # Module registry for Telegram
│   │   └── module_loader.py   # Auto-loader for Telegram modules
│   └── voice/                 # Voice API endpoints (optional, requires httpx)
│       └── v1/
│           └── routes.py      # Voice processing endpoints
│
├── core/                      # Shared core libraries (used by all modules)
│   ├── state/v1/              # State management (SQLite)
│   ├── db/v1/                 # Key-value database
│   ├── voice_gateway/v1/      # Voice/LLM pipeline (DeepSeek integration)
│   └── integrations/          # HTTP client and environment utilities
│       ├── patch_v3/          # Legacy HTTP client
│       └── patch_v4/          # Current HTTP client
│
├── modules/                   # Training modules
│   ├── master_path/v3/        # Full sales cycle training
│   ├── arena/v4/              # AI client simulation
│   ├── objections/v3/         # Objection handling
│   ├── upsell/v3/             # Upselling training
│   ├── sleeping_dragon/v4/    # Sales mistake detector
│   ├── exam_autocheck/v2/     # Automated exam grading
│   ├── trainer_*/v1/          # Advanced trainer modules
│   ├── voice_arena/v1/        # Voice-based training
│   ├── dialog_memory/v1/      # Conversation history
│   ├── edu_lessons/v1/        # Educational content
│   ├── client_cases/v1/       # Real client scenarios
│   └── deepseek_persona/v1/   # Brand voice/persona
│
├── integrations/              # External integrations
│   ├── telegram_bot/v1/       # Telegram bot routes
│   └── telegram_push/v1/      # Push notifications
│
├── telegram/                  # Telegram bot helpers
│   ├── autoload.py            # Auto-register Telegram handlers
│   ├── telegram_main_menu.py  # Main menu handler
│   └── telegram_message_router.py  # Message routing
│
└── smoke_tests/               # Integration tests
```

## Module Versioning

Modules use semantic versioning (v1, v2, v3, v4). The system explicitly imports versioned modules to ensure stability:
- `router_autoload.py` specifies which version of each module to load
- Some modules have `_current/` directories which are legacy aliases (mostly unused)
- Only `deepseek_persona` actively uses the `_current` alias for Telegram integration

## Two Entry Points

### 1. FastAPI Backend (startup.py)
```bash
python main.py
# or
uvicorn startup:app --host 0.0.0.0 --port 8080
```

**Flow:**
1. `startup.py` creates FastAPI app
2. `router_autoload.include_all(app)` registers all module routes
3. Each module in `ROUTE_MODULES` list is imported
4. Module's `router` object is mounted to the app

**Used by:** Web clients, external services, testing

### 2. Telegram Bot (telegram_bot.py)
```bash
python telegram_bot.py
```

**Flow:**
1. Creates aiogram Bot and Dispatcher
2. Creates `ModuleRegistry` from `api.core.registry`
3. Registers main menu handlers
4. Calls `autoload_telegram_handlers()` which:
   - Imports each module
   - Calls `register_telegram(dp, registry)` if it exists
5. Starts polling Telegram API

**Used by:** Telegram users for interactive training

## Configuration

All configuration is done through environment variables:

### Required:
- `TELEGRAM_BOT_TOKEN` - Telegram bot token from @BotFather
- `DEEPSEEK_API_KEY` - DeepSeek API key for AI features

### Optional:
- `DEEPSEEK_MODEL` - Model name (default: "deepseek-chat")
- `DEEPSEEK_API_URL` - API endpoint
- `VOICE_API_KEY` - For voice features
- `BACKEND_URL` - Backend URL (default: http://127.0.0.1:8080)

See `start_core_api.bat` for example configuration.

## Module Integration

### For FastAPI:
Each module should have a `routes.py` with:
```python
from fastapi import APIRouter

router = APIRouter(prefix="/module_name/v1", tags=["module"])

@router.get("/endpoint")
async def handler():
    return {"ok": True}
```

Then add to `ROUTE_MODULES` list in `router_autoload.py`.

### For Telegram:
Each module should have in its `__init__.py`:
```python
def register_telegram(dp, registry):
    from aiogram import types
    
    @dp.message(Command("command_name"))
    async def handler(message: types.Message):
        await message.answer("Response")
```

The `telegram/autoload.py` will automatically discover and register it.

## Core Libraries

All modules import from `core/` for shared functionality:

```python
# State management
from core.state.v1 import StateStore

# Voice/LLM pipeline
from core.voice_gateway.v1 import VoicePipeline

# HTTP client
from core.integrations.patch_v4.http_client import http_post, http_get

# Database
from core.db.v1 import DB
```

## Cleanup History

**2024-11-21:** Removed unused files:
- `api/core/voice_gateway/` - Duplicate of `core/voice_gateway/`
- `api/main.py` - Unused FastAPI entry point
- `api/core/main.py` - Unused FastAPI entry point  
- `api/core/settings.py` - Unused settings file
- `README_CORE.txt` - Outdated documentation

The `api/core/` directory now only contains:
- `registry.py` - Module registry (used by Telegram bot)
- `module_loader.py` - Module loader (used by Telegram bot)

## Running the Application

**Windows:**
```cmd
start_core_api.bat
```

This starts both:
1. FastAPI backend on port 8080
2. Telegram bot

**Linux/Mac:**
```bash
# Terminal 1: Backend
export TELEGRAM_BOT_TOKEN="your_token"
export DEEPSEEK_API_KEY="your_key"
python main.py

# Terminal 2: Telegram Bot
export TELEGRAM_BOT_TOKEN="your_token"
export DEEPSEEK_API_KEY="your_key"
python telegram_bot.py
```

## Testing

```bash
# Check configuration
python validate_setup.py

# Test imports
python -c "from startup import app; print('OK')"
python -c "from api.core.registry import ModuleRegistry; print('OK')"

# Run smoke tests
python smoke_tests/basic.py http://127.0.0.1:8080
```

## API Endpoints

See full API documentation at: `http://localhost:8080/docs`

Key endpoints:
- `GET /api/public/v1/health` - Health check
- `GET /api/public/v1/routes_summary` - List of loaded routes
- `GET /docs` - Interactive API documentation (Swagger UI)

## Further Documentation

- `README.md` - Quick start guide
- `QUICK_START.md` - 5-minute setup guide
- `TELEGRAM_BOT_GUIDE.md` - Telegram bot usage
- `STARTUP_OPTIONS.md` - Troubleshooting
- `IMPLEMENTATION_SUMMARY.md` - Technical details
