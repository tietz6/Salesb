from fastapi import FastAPI, Request
import os

app = FastAPI(title="salesbot", version="v1-final")

# Telegram bot integration
bot = None
dp = None
registry = None

def setup_telegram_bot():
    """Initialize telegram bot with all handlers"""
    global bot, dp, registry
    
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_TOKEN:
        print("[startup] WARNING: TELEGRAM_TOKEN not set, telegram bot will not work")
        return False
    
    try:
        from aiogram import Bot, Dispatcher
        from api.core.registry import ModuleRegistry
        from telegram.autoload import autoload_telegram_handlers
        from telegram_main_menu import register_main_menu
        from telegram_message_router import register_message_router
        
        bot = Bot(token=TELEGRAM_TOKEN)
        dp = Dispatcher()
        registry = ModuleRegistry()
        
        print("[startup] Registering main menu and commands...")
        register_main_menu(dp, registry)
        
        print("[startup] Auto-loading module handlers...")
        autoload_telegram_handlers(dp, registry, package_name="modules")
        
        print("[startup] Registering message router...")
        register_message_router(dp, registry)
        
        print("[startup] Telegram bot initialized successfully!")
        return True
    except Exception as e:
        print(f"[startup] Failed to initialize telegram bot: {e}")
        return False

# Initialize telegram bot on startup
telegram_initialized = setup_telegram_bot()

# базовый healthcheck
@app.get("/api/public/v1/health")
async def root_health():
    return {
        "ok": True, 
        "app": "salesbot", 
        "version": "v1-final",
        "telegram_bot": "enabled" if telegram_initialized else "disabled"
    }

# Telegram webhook endpoint
@app.post("/api/telegram/webhook")
async def telegram_webhook(request: Request):
    """Handle incoming telegram updates via webhook"""
    if not telegram_initialized or not bot or not dp:
        return {"ok": False, "error": "telegram bot not initialized"}
    
    try:
        update_data = await request.json()
        
        # Import Update class
        from aiogram.types import Update
        
        # Create Update object from dict
        update = Update(**update_data)
        
        # Feed update to dispatcher
        # Note: This will process the update and trigger handlers
        # The handlers will attempt to send responses back to Telegram
        await dp.feed_update(bot, update)
        
        # Return success - the actual response to user is sent by the handlers
        # If there's a network error sending to Telegram, it's logged but we still
        # return 200 OK to Telegram so they know we received the update
        return {"ok": True}
    except Exception as e:
        # Log the error but still return success to Telegram
        # This prevents Telegram from resending the same update
        print(f"[telegram_webhook] Error processing update: {e}")
        import traceback
        traceback.print_exc()
        
        # Return OK to Telegram even on error, to prevent retry loops
        # The error is logged for debugging
        return {"ok": True, "error_logged": str(e)}

# автоподключение всех роутов
try:
    from router_autoload import include_all
    include_all(app)
except Exception as e:
    @app.get("/api/public/v1/router_error")
    async def router_error():
        return {"ok": False, "error": str(e)}

# опциональный автобилдер
try:
    from autobuilder.routes import router as autobuilder_router
    app.include_router(autobuilder_router)
except Exception:
    pass