"""
Запуск Telegram-бота как отдельного процесса.
- Требуется установить переменную окружения TELEGRAM_TOKEN.
- Используем aiogram v3 (Dispatcher + dp.start_polling с async/await).
"""
import os
import sys
import asyncio

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    print("ERROR: set TELEGRAM_TOKEN or TELEGRAM_BOT_TOKEN environment variable")
    sys.exit(1)

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

# Подключаем автозагрузчик модулей для telegram
from telegram.autoload import autoload_telegram_handlers
from api.core.registry import ModuleRegistry
from telegram_main_menu import register_main_menu
from telegram_message_router import register_message_router

async def main():
    # Check for custom API server (for proxy or local bot API)
    TELEGRAM_API_SERVER = os.getenv("TELEGRAM_API_SERVER")
    
    # Create bot instance with optional custom API server
    if TELEGRAM_API_SERVER:
        print(f"[run_bot] Using custom API server: {TELEGRAM_API_SERVER}")
        session = AiohttpSession(
            api=TelegramAPIServer.from_base(TELEGRAM_API_SERVER, is_local=True)
        )
        bot = Bot(token=TELEGRAM_TOKEN, session=session)
    else:
        bot = Bot(token=TELEGRAM_TOKEN)
    
    dp = Dispatcher()
    registry = ModuleRegistry()
    
    # Test connection first
    try:
        print("[run_bot] Testing connection to Telegram API...")
        me = await bot.get_me()
        print(f"[run_bot] ✅ Successfully connected to Telegram API!")
        print(f"[run_bot] Bot Info:")
        print(f"[run_bot]   - ID: {me.id}")
        print(f"[run_bot]   - Name: {me.first_name}")
        print(f"[run_bot]   - Username: @{me.username}")
    except Exception as e:
        print(f"[run_bot] ❌ ERROR: Failed to connect to Telegram API")
        print(f"[run_bot] Error: {e}")
        print(f"[run_bot]")
        print(f"[run_bot] 💡 Solutions:")
        print(f"[run_bot]   1. Check your bot token")
        print(f"[run_bot]   2. Verify internet connectivity")
        print(f"[run_bot]   3. Set up a proxy or use local Bot API server")
        print(f"[run_bot]   4. Run: python test_telegram_connection.py for detailed diagnosis")
        await bot.session.close()
        sys.exit(1)

    print("[run_bot] Registering main menu and commands...")
    # Регистрируем главное меню
    register_main_menu(dp, registry)

    print("[run_bot] Auto-loading module handlers...")
    # Автозагрузка телеграм-хэндлеров из пакета modules
    autoload_telegram_handlers(dp, registry, package_name="modules")

    print("[run_bot] Registering message router...")
    # Регистрируем обработчик сообщений для активных сессий
    register_message_router(dp, registry)

    print("[run_bot] Starting polling...")
    try:
        await dp.start_polling(bot, skip_updates=True)
    except KeyboardInterrupt:
        print("\n[run_bot] Bot stopped by user")
    except Exception as e:
        print(f"\n[run_bot] ❌ ERROR during polling: {e}")
    finally:
        await bot.session.close()
        print("[run_bot] Bot session closed")
    print("[run_bot] Stopped polling.")

if __name__ == "__main__":
    asyncio.run(main())