"""
Сервис модуля F3 — Эмоциональная коммуникация
Предоставляет функции для работы с уроками, тестами и прогрессом

Тон: тёплый, заботливый, неформальный, но профессиональный
"""

import logging
from typing import Dict, Any, List, Optional

# Импортируем данные модуля F3
from .module_f3_emotion import (
    MODULE_F3_EMOTION,
    get_module as _get_module_data,
    get_lesson as _get_lesson_data,
    get_test as _get_test_data
)

log = logging.getLogger(__name__)


def get_module() -> Dict[str, Any]:
    """
    Возвращает метаданные модуля F3 с уроками и тестами.
    
    Returns:
        dict: Словарь с метаданными модуля:
            - id: идентификатор модуля
            - title: название модуля
            - description: описание
            - level: уровень сложности
            - estimated_duration_minutes: примерное время прохождения
            - keywords: ключевые слова
            - lessons: список уроков
            - tests: список тестов
    """
    try:
        module_data = _get_module_data()
        return {
            "id": module_data.get("id"),
            "title": module_data.get("title"),
            "description": module_data.get("description"),
            "level": module_data.get("level"),
            "estimated_duration_minutes": module_data.get("estimated_duration_minutes"),
            "keywords": module_data.get("keywords", []),
            "lessons": [
                {
                    "id": lesson["id"],
                    "title": lesson["title"],
                    "duration_minutes": lesson.get("duration_minutes"),
                    "order": idx + 1
                }
                for idx, lesson in enumerate(module_data.get("lessons", []))
            ],
            "tests": [
                {
                    "id": test["id"],
                    "title": test["title"],
                    "passing_score": test.get("passing_score"),
                    "questions_count": len(test.get("questions", []))
                }
                for test in module_data.get("tests", [])
            ]
        }
    except Exception as e:
        log.exception("Ошибка при получении данных модуля F3: %s", e)
        raise


def get_lesson(module_id: str, lesson_id: str) -> Optional[Dict[str, Any]]:
    """
    Возвращает данные одного урока по его ID.
    
    Args:
        module_id: ID модуля (для проверки)
        lesson_id: ID урока
        
    Returns:
        dict: Словарь с данными урока:
            - title: название урока
            - content_ru: содержимое урока на русском
            - order: порядковый номер урока
        None: если урок не найден
    """
    try:
        # Проверяем, что запрашивается модуль F3
        if module_id != "module_f3_emotion":
            log.warning("Запрос урока для неизвестного модуля: %s", module_id)
            return None
        
        lesson = _get_lesson_data(lesson_id)
        if lesson is None:
            log.warning("Урок не найден: %s", lesson_id)
            return None
        
        # Находим порядковый номер урока
        module_data = _get_module_data()
        order = 1
        for idx, l in enumerate(module_data.get("lessons", [])):
            if l["id"] == lesson_id:
                order = idx + 1
                break
        
        return {
            "id": lesson["id"],
            "title": lesson["title"],
            "content_ru": lesson.get("content_ru", ""),
            "order": order,
            "duration_minutes": lesson.get("duration_minutes"),
            "examples": lesson.get("examples", [])
        }
    except Exception as e:
        log.exception("Ошибка при получении урока %s: %s", lesson_id, e)
        raise


def start_lesson_for_user(user_id: str, module_id: str, lesson_id: str) -> Dict[str, Any]:
    """
    Логирует начало прохождения урока пользователем.
    
    TODO: В будущем здесь можно добавить сохранение прогресса в БД.
    
    Args:
        user_id: ID пользователя
        module_id: ID модуля
        lesson_id: ID урока
        
    Returns:
        dict: Статус операции с полями:
            - success: True если операция успешна
            - message: сообщение о результате
    """
    try:
        # Проверяем, что урок существует
        lesson = get_lesson(module_id, lesson_id)
        if lesson is None:
            log.warning("Попытка начать несуществующий урок: user=%s, module=%s, lesson=%s",
                       user_id, module_id, lesson_id)
            return {
                "success": False,
                "message": "Урок не найден"
            }
        
        # TODO: Сохранить прогресс в БД
        log.info("✓ Пользователь %s начал урок %s модуля %s", user_id, lesson_id, module_id)
        
        return {
            "success": True,
            "message": f"Урок '{lesson['title']}' начат успешно",
            "lesson_id": lesson_id,
            "user_id": user_id
        }
    except Exception as e:
        log.exception("Ошибка при старте урока: user=%s, lesson=%s: %s", user_id, lesson_id, e)
        raise


def submit_test(user_id: str, module_id: str, test_id: str, answers: List[int]) -> Dict[str, Any]:
    """
    Валидирует ответы пользователя на тест и возвращает результат.
    Проходной балл — 70%.
    
    Args:
        user_id: ID пользователя
        module_id: ID модуля
        test_id: ID теста
        answers: Список ответов пользователя (индексы выбранных вариантов)
        
    Returns:
        dict: Результат прохождения теста:
            - score: набранный балл (процент)
            - passed: пройден ли тест (True/False)
            - correct_answers: количество правильных ответов
            - user_answers: ответы пользователя
            - total_questions: общее количество вопросов
    """
    try:
        # Проверяем, что это модуль F3
        if module_id != "module_f3_emotion":
            log.warning("Попытка отправить тест для неизвестного модуля: %s", module_id)
            return {
                "success": False,
                "message": "Модуль не найден"
            }
        
        # Получаем тест
        test = _get_test_data()
        if test is None or test.get("id") != test_id:
            log.warning("Тест не найден: %s", test_id)
            return {
                "success": False,
                "message": "Тест не найден"
            }
        
        questions = test.get("questions", [])
        total_questions = len(questions)
        passing_score = test.get("passing_score", 70)
        
        # Проверяем количество ответов
        if len(answers) != total_questions:
            log.warning("Неверное количество ответов: ожидалось %d, получено %d",
                       total_questions, len(answers))
            return {
                "success": False,
                "message": f"Неверное количество ответов: ожидалось {total_questions}, получено {len(answers)}"
            }
        
        # Считаем правильные ответы
        correct_answers = 0
        results = []
        for idx, question in enumerate(questions):
            user_answer = answers[idx] if idx < len(answers) else None
            correct = question.get("correct")
            is_correct = user_answer == correct
            if is_correct:
                correct_answers += 1
            results.append({
                "question_id": question.get("id"),
                "correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": correct,
                "explanation": question.get("explanation") if not is_correct else None
            })
        
        # Вычисляем процент
        score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
        passed = score >= passing_score
        
        # TODO: Сохранить результат в БД
        log.info("✓ Пользователь %s завершил тест %s: score=%d%%, passed=%s",
                user_id, test_id, score, passed)
        
        return {
            "success": True,
            "score": score,
            "passed": passed,
            "correct_answers": correct_answers,
            "user_answers": answers,
            "total_questions": total_questions,
            "passing_score": passing_score,
            "details": results
        }
    except Exception as e:
        log.exception("Ошибка при проверке теста: user=%s, test=%s: %s", user_id, test_id, e)
        raise
