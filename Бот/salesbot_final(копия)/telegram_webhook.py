"""
Telegram bot с использованием Webhook вместо long polling
Используйте этот файл если polling не работает из-за сетевых ограничений
"""
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from api.core.registry import ModuleRegistry
from telegram.autoload import autoload_telegram_handlers
from telegram_main_menu import register_main_menu
from telegram_message_router import register_message_router

# Конфигурация
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    print("ERROR: set TELEGRAM_TOKEN or TELEGRAM_BOT_TOKEN environment variable")
    sys.exit(1)

# URL вебхука - должен быть публичным HTTPS URL
# Примеры:
# - https://yourdomain.com
# - https://abc123.ngrok.io (для тестирования с ngrok)
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://localhost:8443")
WEBHOOK_PATH = f"/bot{TELEGRAM_TOKEN}"

# Порт для webhook сервера
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8443"))
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "0.0.0.0")

# SSL сертификаты (опционально, если используете самоподписанный сертификат)
SSL_CERT_PATH = os.getenv("SSL_CERT_PATH")
SSL_KEY_PATH = os.getenv("SSL_KEY_PATH")

# Создаем экземпляры
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
registry = ModuleRegistry()

print("[telegram_webhook] Initializing bot...")
print(f"[telegram_webhook] Webhook URL: {WEBHOOK_URL}{WEBHOOK_PATH}")
print(f"[telegram_webhook] Webhook will listen on: {WEBHOOK_HOST}:{WEBHOOK_PORT}")


async def on_startup(bot: Bot):
    """
    Вызывается при запуске бота - устанавливает webhook
    """
    webhook_url = f"{WEBHOOK_URL}{WEBHOOK_PATH}"
    
    try:
        # Проверяем подключение к Telegram API
        me = await bot.get_me()
        print(f"[telegram_webhook] ✅ Bot connected: @{me.username}")
        
        # Устанавливаем webhook
        if SSL_CERT_PATH:
            # Если используется самоподписанный сертификат
            with open(SSL_CERT_PATH, 'rb') as cert_file:
                await bot.set_webhook(
                    url=webhook_url,
                    certificate=cert_file
                )
        else:
            # Обычная установка webhook
            await bot.set_webhook(url=webhook_url)
        
        # Проверяем установку webhook
        webhook_info = await bot.get_webhook_info()
        print(f"[telegram_webhook] ✅ Webhook set successfully!")
        print(f"[telegram_webhook]    URL: {webhook_info.url}")
        print(f"[telegram_webhook]    Pending updates: {webhook_info.pending_update_count}")
        
        if webhook_info.last_error_date:
            print(f"[telegram_webhook] ⚠️  Last error: {webhook_info.last_error_message}")
        
    except Exception as e:
        print(f"[telegram_webhook] ❌ ERROR: Failed to set webhook")
        print(f"[telegram_webhook] Error: {e}")
        print(f"[telegram_webhook]")
        print(f"[telegram_webhook] 💡 Make sure:")
        print(f"[telegram_webhook]    1. WEBHOOK_URL is a valid HTTPS URL")
        print(f"[telegram_webhook]    2. Your server is accessible from the internet")
        print(f"[telegram_webhook]    3. Port {WEBHOOK_PORT} is open")
        print(f"[telegram_webhook]    4. You have a valid SSL certificate")
        print(f"[telegram_webhook]")
        print(f"[telegram_webhook] For testing, use ngrok:")
        print(f"[telegram_webhook]    ngrok http {WEBHOOK_PORT}")
        print(f"[telegram_webhook]    Then set WEBHOOK_URL to the ngrok URL")
        raise


async def on_shutdown(bot: Bot):
    """
    Вызывается при остановке бота - удаляет webhook
    """
    try:
        await bot.delete_webhook()
        print("[telegram_webhook] Webhook removed")
    except Exception as e:
        print(f"[telegram_webhook] Error removing webhook: {e}")
    
    await bot.session.close()


def main():
    """
    Основная функция запуска webhook сервера
    """
    print("[telegram_webhook] Registering handlers...")
    
    # Регистрируем главное меню
    register_main_menu(dp, registry)
    
    # Автозагрузка модулей
    autoload_telegram_handlers(dp, registry, package_name="modules")
    
    # Регистрируем message router
    register_message_router(dp, registry)
    
    print("[telegram_webhook] All handlers registered")
    
    # Регистрируем startup и shutdown обработчики
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Создаем aiohttp приложение
    app = web.Application()
    
    # Настраиваем webhook обработчик
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    
    # Добавляем healthcheck endpoint
    async def health_check(request):
        return web.json_response({"status": "ok", "bot": "telegram_webhook"})
    
    app.router.add_get('/health', health_check)
    
    print("[telegram_webhook] Starting webhook server...")
    print(f"[telegram_webhook] Listening on {WEBHOOK_HOST}:{WEBHOOK_PORT}")
    print(f"[telegram_webhook] Healthcheck: http://{WEBHOOK_HOST}:{WEBHOOK_PORT}/health")
    print(f"[telegram_webhook]")
    print(f"[telegram_webhook] 🚀 Bot is ready to receive updates!")
    print(f"[telegram_webhook] Send messages to your bot in Telegram")
    print(f"[telegram_webhook]")
    
    # Запускаем сервер
    try:
        if SSL_CERT_PATH and SSL_KEY_PATH:
            # С SSL сертификатом
            import ssl
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(SSL_CERT_PATH, SSL_KEY_PATH)
            web.run_app(app, host=WEBHOOK_HOST, port=WEBHOOK_PORT, ssl_context=ssl_context)
        else:
            # Без SSL (для использования с ngrok или за reverse proxy)
            web.run_app(app, host=WEBHOOK_HOST, port=WEBHOOK_PORT)
    except KeyboardInterrupt:
        print("\n[telegram_webhook] Bot stopped by user")
    except Exception as e:
        print(f"\n[telegram_webhook] ❌ ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
