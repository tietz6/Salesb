"""
Router модуля F3 — Эмоциональная коммуникация
FastAPI эндпоинты для работы с модулем обучения эмоциональной коммуникации

API пути: /academy/v1/modules/module_f3_emotion
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from .module_f3_service import (
    get_module,
    get_lesson,
    start_lesson_for_user,
    submit_test
)

log = logging.getLogger(__name__)

# Основной роутер с версионированным путём
router = APIRouter(prefix="/academy/v1/modules/module_f3_emotion", tags=["academy_modules"])

# Дополнительный роутер без версии для совместимости
router_noversion = APIRouter(prefix="/academy/modules/module_f3_emotion", tags=["academy_modules"])


# Pydantic модели для валидации входных данных
class TestSubmission(BaseModel):
    """Модель для отправки результатов теста"""
    user_id: str
    answers: List[int]


# ==================== Версионированные эндпоинты ====================

@router.get("/")
async def api_get_module():
    """
    Возвращает метаданные модуля F3 с информацией об уроках и тестах.
    
    Returns:
        JSON с метаданными модуля, списком уроков и тестов
    """
    try:
        module_data = get_module()
        return {
            "ok": True,
            "module": module_data
        }
    except Exception as e:
        log.exception("Ошибка при получении модуля: %s", e)
        raise HTTPException(status_code=500, detail="Ошибка при получении данных модуля")


@router.get("/lessons/{lesson_id}")
async def api_get_lesson(lesson_id: str):
    """
    Возвращает данные конкретного урока по его ID.
    
    Args:
        lesson_id: ID урока (например, lesson_1, lesson_2 и т.д.)
        
    Returns:
        JSON с данными урока (title, content_ru, order)
    """
    try:
        lesson = get_lesson("module_f3_emotion", lesson_id)
        if lesson is None:
            raise HTTPException(status_code=404, detail=f"Урок с ID '{lesson_id}' не найден")
        
        return {
            "ok": True,
            "lesson": lesson
        }
    except HTTPException:
        raise
    except Exception as e:
        log.exception("Ошибка при получении урока %s: %s", lesson_id, e)
        raise HTTPException(status_code=500, detail="Ошибка при получении урока")


@router.post("/progress/{user_id}/lessons/{lesson_id}/start")
async def api_start_lesson(user_id: str, lesson_id: str):
    """
    Регистрирует начало прохождения урока пользователем.
    
    Args:
        user_id: ID пользователя
        lesson_id: ID урока
        
    Returns:
        JSON со статусом операции
    """
    try:
        result = start_lesson_for_user(user_id, "module_f3_emotion", lesson_id)
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("message", "Ошибка"))
        
        return {
            "ok": True,
            "result": result
        }
    except HTTPException:
        raise
    except Exception as e:
        log.exception("Ошибка при старте урока: user=%s, lesson=%s: %s", user_id, lesson_id, e)
        raise HTTPException(status_code=500, detail="Ошибка при старте урока")


@router.post("/tests/{test_id}/submit")
async def api_submit_test(test_id: str, submission: TestSubmission):
    """
    Проверяет ответы пользователя на тест и возвращает результат.
    
    Args:
        test_id: ID теста
        submission: JSON с user_id и массивом ответов
        
    Returns:
        JSON с результатом теста:
            - score: набранный балл (%)
            - passed: пройден ли тест
            - correct_answers: количество правильных ответов
            - total_questions: общее количество вопросов
    """
    try:
        result = submit_test(
            user_id=submission.user_id,
            module_id="module_f3_emotion",
            test_id=test_id,
            answers=submission.answers
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Ошибка при проверке теста")
            )
        
        return {
            "ok": True,
            "result": result
        }
    except HTTPException:
        raise
    except Exception as e:
        log.exception("Ошибка при проверке теста %s: %s", test_id, e)
        raise HTTPException(status_code=500, detail="Ошибка при проверке теста")


# Telegram bot интеграция
@router.post("/start")
async def start_telegram(req: Request):
    """Telegram bot integration endpoint - accepts chat_id"""
    data = await req.json()
    probe = data.get("probe", False)
    
    # Quick response for probe requests (discovery)
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Academy F3 Emotion module - use /lessons, /tests endpoints"}


@router.post("/start_session")
async def start_session(req: Request):
    """Session start endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Academy F3 Emotion module - use /lessons, /tests endpoints"}


@router.post("/run")
async def run(req: Request):
    """Run endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Academy F3 Emotion module - use /lessons, /tests endpoints"}


@router.post("/init")
async def init(req: Request):
    """Init endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Academy F3 Emotion module - use /lessons, /tests endpoints"}


# ==================== Не-версионированные эндпоинты ====================

@router_noversion.get("/")
async def api_get_module_noversion():
    """Не-версионированный эндпоинт для получения модуля"""
    return await api_get_module()


@router_noversion.get("/lessons/{lesson_id}")
async def api_get_lesson_noversion(lesson_id: str):
    """Не-версионированный эндпоинт для получения урока"""
    return await api_get_lesson(lesson_id)


@router_noversion.post("/progress/{user_id}/lessons/{lesson_id}/start")
async def api_start_lesson_noversion(user_id: str, lesson_id: str):
    """Не-версионированный эндпоинт для старта урока"""
    return await api_start_lesson(user_id, lesson_id)


@router_noversion.post("/tests/{test_id}/submit")
async def api_submit_test_noversion(test_id: str, submission: TestSubmission):
    """Не-версионированный эндпоинт для отправки теста"""
    return await api_submit_test(test_id, submission)


@router_noversion.post("/start")
async def start_telegram_noversion(req: Request):
    """Telegram bot integration endpoint - не-версионированный"""
    return await start_telegram(req)


@router_noversion.post("/start_session")
async def start_session_noversion(req: Request):
    """Session start endpoint - не-версионированный"""
    return await start_session(req)


@router_noversion.post("/run")
async def run_noversion(req: Request):
    """Run endpoint - не-версионированный"""
    return await run(req)


@router_noversion.post("/init")
async def init_noversion(req: Request):
    """Init endpoint - не-версионированный"""
    return await init(req)
