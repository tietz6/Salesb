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

# Подключаем автозагрузчик модулей для telegram
from telegram.autoload import autoload_telegram_handlers
from api.core.registry import ModuleRegistry
from telegram_main_menu import register_main_menu
from telegram_message_router import register_message_router

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    registry = ModuleRegistry()

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
    await dp.start_polling(bot, skip_updates=True)
    print("[run_bot] Stopped polling.")

if __name__ == "__main__":
    asyncio.run(main())