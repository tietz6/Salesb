import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from api.core.registry import ModuleRegistry
from telegram.autoload import autoload_telegram_handlers
from telegram_main_menu import register_main_menu
from telegram_message_router import register_message_router

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN or TELEGRAM_BOT_TOKEN environment variable required")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
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

def run():
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
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    run()