"""
Message router for telegram bot - routes messages to active training sessions
"""
try:
    from aiogram import types, F
    from aiogram import Dispatcher
    AIOGRAM_AVAILABLE = True
except ImportError:
    AIOGRAM_AVAILABLE = False
    types = None
    Dispatcher = None
    F = None


# Global session tracker
USER_ACTIVE_SESSIONS = {}


def register_message_router(dp, registry):
    """
    Регистрирует обработчик сообщений для активных тренировочных сессий
    """
    if not AIOGRAM_AVAILABLE:
        return
    
    @dp.message(F.text & ~F.text.startswith('/'))
    async def _route_message_to_active_session(message: types.Message):
        """
        Маршрутизирует обычные текстовые сообщения к активным сессиям тренировок
        """
        user_id = str(message.from_user.id)
        active_session = USER_ACTIVE_SESSIONS.get(user_id)
        
        if not active_session:
            # Нет активной сессии
            await message.reply(
                "🤔 Активной тренировки нет.\n\n"
                "Выбери модуль для начала:\n"
                "/master_path - Путь Мастера\n"
                "/arena - Арена с AI\n"
                "/objections - Работа с возражениями\n"
                "/upsell - Допродажи\n\n"
                "Или используй /menu для полного меню"
            )
            return
        
        # Обрабатываем сообщение в зависимости от активной сессии
        session_type = active_session.get('type')
        
        try:
            if session_type == 'master_path':
                await _handle_master_path_message(message, user_id)
            elif session_type == 'arena':
                await _handle_arena_message(message, user_id)
            elif session_type == 'objections':
                await _handle_objections_message(message, user_id)
            elif session_type == 'upsell':
                await _handle_upsell_message(message, user_id)
            else:
                await message.reply(
                    f"❌ Неизвестный тип сессии: {session_type}\n"
                    "Используй /menu чтобы начать заново"
                )
        except Exception as e:
            await message.reply(
                f"❌ Ошибка при обработке: {str(e)}\n\n"
                "Попробуй начать заново с /menu"
            )
    
    async def _handle_master_path_message(message: types.Message, user_id: str):
        """Обработка сообщения для Master Path"""
        from modules.master_path.v3.engine import MasterPath
        
        mp = MasterPath(user_id)
        result = mp.handle(message.text)
        
        stages_ru = {
            "greeting": "Приветствие",
            "qualification": "Квалификация",
            "support": "Поддержка",
            "offer": "Предложение",
            "demo": "Демо",
            "final": "Закрытие",
            "done": "Завершено"
        }
        
        stage_name = stages_ru.get(result['stage'], result['stage'])
        coach_suggestion = result.get('coach_suggestion', '')
        score = result.get('score', 0)
        
        response = f"📍 Этап: *{stage_name}*\n"
        
        if score > 0:
            response += f"⭐ Оценка: {score} балл(а)\n\n"
        
        if coach_suggestion:
            response += f"🎓 *Совет коуча:*\n{coach_suggestion}\n\n"
        else:
            response += "✅ Хорошо! Продолжай в том же духе.\n\n"
        
        response += "Используй /mp_next для перехода на следующий этап\n"
        response += "или /mp_reset для начала заново"
        
        await message.reply(response, parse_mode="Markdown")
    
    async def _handle_arena_message(message: types.Message, user_id: str):
        """Обработка сообщения для Arena"""
        from modules.arena.v4.engine import ArenaEngine
        
        arena = ArenaEngine(user_id)
        result = arena.handle(message.text)
        
        client_reply = result.get('client_reply', '')
        emotion = result.get('emotion', 'neutral')
        score = result.get('score', 0)
        
        emotions_ru = {
            "calm": "😌 Спокоен",
            "neutral": "😐 Нейтрален",
            "annoyed": "😠 Раздражен",
            "angry": "😡 Зол",
            "excited": "😄 Взволнован"
        }
        
        emotion_name = emotions_ru.get(emotion, emotion)
        
        response = f"👤 *Клиент ({emotion_name}):*\n"
        
        if client_reply:
            response += f"{client_reply}\n\n"
        else:
            response += "Клиент слушает...\n\n"
        
        if score > 0:
            response += f"⭐ Твой балл: {score}\n\n"
        
        response += "Продолжай диалог!\n"
        response += "/arena_reset - новый клиент"
        
        await message.reply(response, parse_mode="Markdown")
    
    async def _handle_objections_message(message: types.Message, user_id: str):
        """Обработка сообщения для Objections"""
        from modules.objections.v3.engine import ObjectionEngine
        
        obj = ObjectionEngine(user_id)
        result = obj.handle(message.text)
        
        client_reply = result.get('client_reply', '')
        score = result.get('score', 0)
        
        response = "👤 *Клиент:*\n"
        
        if client_reply:
            response += f"{client_reply}\n\n"
        else:
            response += "Клиент думает...\n\n"
        
        if score > 0:
            response += f"⭐ Твой балл: {score}\n\n"
        
        response += "Продолжай работу с возражением!\n"
        response += "/obj_reset - новое возражение"
        
        await message.reply(response, parse_mode="Markdown")
    
    async def _handle_upsell_message(message: types.Message, user_id: str):
        """Обработка сообщения для Upsell"""
        from modules.upsell.v3.engine import UpsellEngine
        
        upsell = UpsellEngine(user_id)
        result = upsell.handle(message.text)
        
        client_reply = result.get('client_reply', '')
        score = result.get('score', 0)
        package = result.get('package', 'unknown')
        
        packages_ru = {
            "basic": "🎵 Basic",
            "premium": "🎬 Premium",
            "gold": "⭐ Gold"
        }
        
        package_name = packages_ru.get(package, package)
        
        response = f"👤 *Клиент (пакет {package_name}):*\n"
        
        if client_reply:
            response += f"{client_reply}\n\n"
        else:
            response += "Клиент думает о предложении...\n\n"
        
        if score > 0:
            response += f"⭐ Твой балл: {score}\n\n"
        
        response += "Продолжай допродажу!\n"
        response += "/upsell_reset - новый сценарий"
        
        await message.reply(response, parse_mode="Markdown")


def set_active_session(user_id: str, session_type: str):
    """
    Устанавливает активную сессию для пользователя
    """
    USER_ACTIVE_SESSIONS[user_id] = {'type': session_type}


def clear_active_session(user_id: str):
    """
    Очищает активную сессию для пользователя
    """
    if user_id in USER_ACTIVE_SESSIONS:
        del USER_ACTIVE_SESSIONS[user_id]


def get_active_session(user_id: str):
    """
    Получает активную сессию для пользователя
    """
    return USER_ACTIVE_SESSIONS.get(user_id)
