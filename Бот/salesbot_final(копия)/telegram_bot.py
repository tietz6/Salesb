import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from api.core.registry import ModuleRegistry
from telegram.autoload import autoload_telegram_handlers
from telegram_main_menu import register_main_menu

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

print("[telegram_bot] All handlers registered. Starting bot...")

def run():
    print(f"[telegram_bot] Bot is running! Connected to Telegram API.")
    print(f"[telegram_bot] Send /start to the bot to begin!")
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    run()