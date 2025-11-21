import os
import asyncio
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from api.core.registry import ModuleRegistry
from telegram.autoload import autoload_telegram_handlers
from telegram_main_menu import register_main_menu
from telegram_message_router import register_message_router

# Get Telegram token from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN or TELEGRAM_BOT_TOKEN environment variable required")

# Check for custom API server (for proxy or local bot API)
TELEGRAM_API_SERVER = os.getenv("TELEGRAM_API_SERVER")

# Create bot instance with optional custom API server
if TELEGRAM_API_SERVER:
    print(f"[telegram_bot] Using custom API server: {TELEGRAM_API_SERVER}")
    # Parse custom API server URL
    session = AiohttpSession(
        api=TelegramAPIServer.from_base(TELEGRAM_API_SERVER, is_local=True)
    )
    bot = Bot(token=TELEGRAM_TOKEN, session=session)
else:
    bot = Bot(token=TELEGRAM_TOKEN)

dp = Dispatcher()
registry = ModuleRegistry()

print("[telegram_bot] Registering main menu and commands...")
# Регистрируем главное меню
register_main_menu(dp, registry)

print("[telegram_bot] Auto-loading module handlers...")
# Автозагрузка модулей
autoload_telegram_handlers(dp, registry, package_name="modules")

print("[telegram_bot] Registering message router...")
# Регистрируем обработчик сообщений для активных сессий
register_message_router(dp, registry)

print("[telegram_bot] All handlers registered. Starting bot...")

async def main():
    """Main bot function with connection verification"""
    try:
        # Test connection to Telegram API
        print(f"[telegram_bot] Testing connection to Telegram API...")
        me = await bot.get_me()
        print(f"[telegram_bot] ✅ Successfully connected to Telegram API!")
        print(f"[telegram_bot] Bot Info:")
        print(f"[telegram_bot]   - ID: {me.id}")
        print(f"[telegram_bot]   - Name: {me.first_name}")
        print(f"[telegram_bot]   - Username: @{me.username}")
        
        # Delete any existing webhook to ensure polling works
        print(f"[telegram_bot] Removing any existing webhook...")
        await bot.delete_webhook(drop_pending_updates=True)
        print(f"[telegram_bot] ✅ Webhook removed (if any existed)")
        
    except Exception as e:
        print(f"[telegram_bot] ❌ ERROR: Failed to connect to Telegram API")
        print(f"[telegram_bot] Error type: {type(e).__name__}")
        print(f"[telegram_bot] Error message: {str(e)}")
        print(f"[telegram_bot]")
        print(f"[telegram_bot] 🔍 Possible causes:")
        print(f"[telegram_bot]   1. Invalid bot token")
        print(f"[telegram_bot]   2. No internet connection")
        print(f"[telegram_bot]   3. Telegram API is blocked (firewall/proxy)")
        print(f"[telegram_bot]   4. DNS resolution issues")
        print(f"[telegram_bot]")
        print(f"[telegram_bot] 💡 Solutions:")
        print(f"[telegram_bot]   1. Check your bot token in start_core_api.bat")
        print(f"[telegram_bot]   2. Verify internet connectivity")
        print(f"[telegram_bot]   3. Set up a proxy or use local Bot API server")
        print(f"[telegram_bot]   4. Set TELEGRAM_API_SERVER environment variable")
        print(f"[telegram_bot]")
        print(f"[telegram_bot] 📖 For more help, see: TELEGRAM_BOT_GUIDE.md")
        
        # Close bot session before exiting
        await bot.session.close()
        sys.exit(1)
    
    print(f"[telegram_bot] Bot is running! Connected to Telegram API.")
    print(f"[telegram_bot] Send /start to the bot to begin!")
    print(f"[telegram_bot] Available commands:")
    print(f"  /start - Main menu")
    print(f"  /master_path - Path of the Master training")
    print(f"  /arena - Arena with AI clients")
    print(f"  /objections - Objections handling")
    print(f"  /upsell - Upselling training")
    print(f"  /products - Product catalog")
    print(f"  /script - Sales script")
    
    try:
        await dp.start_polling(bot, skip_updates=True)
    except KeyboardInterrupt:
        print(f"\n[telegram_bot] Bot stopped by user")
    except Exception as e:
        print(f"\n[telegram_bot] ❌ ERROR during polling: {e}")
    finally:
        await bot.session.close()
        print(f"[telegram_bot] Bot session closed")

def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()