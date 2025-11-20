# Пример шаблона для модуля upsell v3
# Сохраните бизнес-логику прежней; ниже — только регистрация телеграм-хэндлеров.

try:
    from aiogram import types
    from aiogram.dispatcher import Dispatcher
    AIOGRAM_AVAILABLE = True
except ImportError:
    AIOGRAM_AVAILABLE = False
    types = None
    Dispatcher = None

# Здесь — импорт бизнес-функций модуля (ленивый внутри хэндлера, чтобы избежать циклов)
def register_telegram(dp, registry):
    """
    Регистрируем все телеграм-хэндлеры, которые относятся к этому модулю.
    Вызывается автозагрузчиком telegram/autoload.py.
    """
    if not AIOGRAM_AVAILABLE:
        return
    
    @dp.message_handler(commands=["upsell"])
    async def _cmd_upsell(message):
        # ленивый импорт бизнес-логики
        try:
            from .service import start_upsell_session  # пример
        except Exception:
            # если нет service — используем заглушку
            async def start_upsell_session(user_id):
                return {"ok": True, "note": "stub"}

        user_id = message.from_user.id
        result = start_upsell_session(user_id)
        # Если result — coroutine, await it
        if hasattr(result, "__await__"):
            result = await result
        await message.reply(f"Upsell started: {result}")