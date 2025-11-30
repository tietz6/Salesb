# API Examples — Модуль F3: Эмоциональная коммуникация

Примеры curl-запросов для работы с модулем F3 (Эмоциональная коммуникация).

## Получить метаданные модуля

```bash
curl http://127.0.0.1:8080/academy/v1/modules/module_f3_emotion/
```

Ответ:
```json
{
  "ok": true,
  "module": {
    "id": "module_f3_emotion",
    "title": "Модуль F3 — Эмоциональная коммуникация",
    "description": "Научитесь работать с эмоциями клиента через текст и голос...",
    "level": "intermediate",
    "estimated_duration_minutes": 60,
    "keywords": ["эмоция", "тон", "эмпатия", "возражения", "диалог"],
    "lessons": [
      {"id": "lesson_1", "title": "Урок 1. Основы эмпатической коммуникации", "order": 1},
      ...
    ],
    "tests": [
      {"id": "test_f3_emotion", "title": "Тест по модулю F3", "passing_score": 70, "questions_count": 10}
    ]
  }
}
```

## Получить урок по ID

```bash
curl http://127.0.0.1:8080/academy/v1/modules/module_f3_emotion/lessons/lesson_1
```

Ответ:
```json
{
  "ok": true,
  "lesson": {
    "id": "lesson_1",
    "title": "Урок 1. Основы эмпатической коммуникации",
    "content_ru": "# Основы эмпатической коммуникации\n\n## Что такое эмпатия в переписке?...",
    "order": 1,
    "duration_minutes": 9,
    "examples": [...]
  }
}
```

## Начать урок для пользователя

```bash
curl -X POST http://127.0.0.1:8080/academy/v1/modules/module_f3_emotion/progress/123/lessons/lesson_1/start
```

Ответ:
```json
{
  "ok": true,
  "result": {
    "success": true,
    "message": "Урок 'Урок 1. Основы эмпатической коммуникации' начат успешно",
    "lesson_id": "lesson_1",
    "user_id": "123"
  }
}
```

## Отправить ответы на тест

```bash
curl -X POST http://127.0.0.1:8080/academy/v1/modules/module_f3_emotion/tests/test_f3_emotion/submit \
  -H "Content-Type: application/json" \
  -d '{"user_id":"123","answers":[1,2,1,2,1,2,1,1,1,2]}'
```

Ответ:
```json
{
  "ok": true,
  "result": {
    "success": true,
    "score": 100,
    "passed": true,
    "correct_answers": 10,
    "user_answers": [1, 2, 1, 2, 1, 2, 1, 1, 1, 2],
    "total_questions": 10,
    "passing_score": 70,
    "details": [
      {"question_id": "q1", "correct": true, "user_answer": 1, "correct_answer": 1, "explanation": null},
      ...
    ]
  }
}
```

## Проверка работоспособности сервера

```bash
curl http://127.0.0.1:8080/api/public/v1/health
```

Ответ:
```json
{"ok": true, "app": "salesbot", "version": "v1-final"}
```

## Получить сводку загруженных роутов

```bash
curl http://127.0.0.1:8080/api/public/v1/routes_summary
```

Ответ:
```json
{
  "attached": [
    "modules.master_path.v3.routes",
    "modules.academy.v1.module_f3_router",
    ...
  ],
  "errors": []
}
```
