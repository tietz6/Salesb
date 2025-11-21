@echo off
setlocal

REM ============================================================================
REM SALESBOT - Unified Startup Script
REM ============================================================================
REM Этот скрипт запускает все необходимые компоненты системы Salesbot:
REM 1. FastAPI Backend Server (порт 8080)
REM 2. Telegram Bot с aiogram 3.x (полный функционал)
REM
REM Для запуска всей системы просто запустите этот файл!
REM ============================================================================

REM --- переходим в папку с проектом ---
cd /d "%~dp0"

REM --- активируем виртуальное окружение ---
echo Активация виртуального окружения...
call venv\Scripts\activate
if errorlevel 1 (
    echo ОШИБКА: Не удалось активировать виртуальное окружение venv
    echo Убедитесь, что папка venv существует и содержит правильное окружение
    echo Для создания: python -m venv venv
    pause
    exit /b 1
)

REM ============================================================================
REM === НАСТРОЙКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ===
REM ============================================================================

REM === DeepSeek AI ===
set DEEPSEEK_API_KEY=sk-4de54b0041b44cf193b22cf21f028be7
set DEEPSEEK_MODEL=deepseek-chat
REM Можно не задавать, у нас в коде есть значение по умолчанию:
REM set DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions

REM === Voice API (для функций голоса) ===
set VOICE_API_KEY=10da831f2d514801a47c79b8e3e68ebb

REM === Telegram Bot Token ===
REM ВАЖНО: Используйте свой токен от @BotFather
REM Все три переменные установлены для совместимости с разными модулями
set TELEGRAM_BOT_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI
set TG_BOT_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI
set TELEGRAM_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI

REM === Дополнительные настройки ===
set TELEGRAM_PUSH_MOCK_MODE=false
set BACKEND_URL=http://127.0.0.1:8080

REM ============================================================================
REM === ПРОВЕРКА НАСТРОЙКИ (ОПЦИОНАЛЬНО) ===
REM ============================================================================

REM Раскомментируйте следующие строки, если хотите запускать валидацию перед стартом:
REM echo Проверка конфигурации...
REM python validate_setup.py
REM if errorlevel 1 (
REM     echo.
REM     echo ОШИБКА: Проверка конфигурации не прошла!
REM     echo Исправьте указанные проблемы и попробуйте снова.
REM     pause
REM     exit /b 1
REM )
REM echo.

REM ============================================================================
REM === ИНФОРМАЦИЯ О ЗАПУСКЕ ===
REM ============================================================================

echo.
echo ============================================================================
echo                    SALESBOT - Запуск всех компонентов
echo ============================================================================
echo.
echo Конфигурация:
echo   Telegram Bot Token: %TELEGRAM_BOT_TOKEN%
echo   DeepSeek API Key: %DEEPSEEK_API_KEY%
echo   Voice API Key: %VOICE_API_KEY%
echo   Backend URL: %BACKEND_URL%
echo.
echo Запускаемые компоненты:
echo   [1/2] FastAPI Backend Server (порт 8080)
echo   [2/2] Telegram Bot с модулями тренировки (aiogram 3.x)
echo.
echo Совет: Для проверки конфигурации запустите: python validate_setup.py
echo.
echo ============================================================================
echo.

REM ============================================================================
REM === ЗАПУСК КОМПОНЕНТОВ ===
REM ============================================================================

REM === Компонент 1: FastAPI Backend Server ===
echo [1/2] Запуск FastAPI сервера на порту 8080...
start "SALESBOT_API" python -m uvicorn startup:app --host 0.0.0.0 --port 8080 --reload
if errorlevel 1 (
    echo ОШИБКА: Не удалось запустить FastAPI сервер
    pause
    exit /b 1
)

REM Пауза для инициализации сервера
echo Ожидание запуска сервера (3 секунды)...
timeout /t 3 /nobreak > nul

REM === Компонент 2: Telegram Bot (aiogram 3.x) ===
echo [2/2] Запуск Telegram бота с модулями тренировки...
start "SALESBOT_TELEGRAM_BOT" python telegram_bot.py
if errorlevel 1 (
    echo ОШИБКА: Не удалось запустить Telegram бота
    pause
    exit /b 1
)

REM ============================================================================
REM === ИНФОРМАЦИЯ ДЛ�Я ПОЛЬЗОВАТЕЛЯ ===
REM ============================================================================

echo.
echo ============================================================================
echo                         Все компоненты запущены!
echo ============================================================================
echo.
echo Открытые окна:
echo   - SALESBOT_API: FastAPI Backend Server (http://localhost:8080)
echo   - SALESBOT_TELEGRAM_BOT: Telegram бот с полным функционалом
echo.
echo Для проверки Backend API откройте в браузере:
echo   http://localhost:8080/api/public/v1/health
echo   http://localhost:8080/docs (документация API)
echo.
echo ============================================================================
echo Доступные команды в Telegram боте:
echo ============================================================================
echo.
echo Главное меню:
echo   /start или /menu - Главное меню со всеми модулями
echo   /products - Каталог продуктов "На Счастье"
echo   /script - Скрипт продаж
echo   /stats - Общая статистика тренировок
echo.
echo Модули тренировок:
echo   /master_path - Путь Мастера (полный цикл продажи)
echo   /arena - Арена с AI-клиентами
echo   /objections - Работа с возражениями
echo   /upsell - Допродажи и апсейлы
echo.
echo AI-Коуч:
echo   /coach ^<вопрос^> - Получить совет от AI-коуча
echo   /stylize ^<текст^> - Стилизация текста под бренд
echo.
echo Управление модулями:
echo   /mp_status, /mp_next, /mp_reset - Управление Master Path
echo   /arena_status, /arena_reset - Управление Arena
echo   /obj_status, /obj_reset - Управление Objections
echo   /upsell_status, /upsell_reset - Управление Upsell
echo.
echo ============================================================================
echo.
echo ============================================================================
echo Управление и Диагностика:
echo ============================================================================
echo.
echo Остановка компонентов:
echo   - Закройте оба окна (SALESBOT_API и SALESBOT_TELEGRAM_BOT)
echo   - Или нажмите Ctrl+C в каждом окне
echo.
echo Проверка работоспособности:
echo   - Проверьте логи в окнах компонентов
echo   - Откройте http://localhost:8080/api/public/v1/health
echo   - Отправьте /start боту в Telegram
echo.
echo Если бот не отвечает:
echo   1. Проверьте логи в окне SALESBOT_TELEGRAM_BOT
echo   2. Убедитесь, что TELEGRAM_BOT_TOKEN правильный
echo   3. Проверьте подключение к интернету
echo   4. Запустите: python validate_setup.py
echo   5. См. STARTUP_OPTIONS.md раздел "Решение проблем"
echo.
echo Документация:
echo   - STARTUP_OPTIONS.md - Варианты запуска и решение проблем
echo   - QUICK_START.md - Быстрый старт за 5 минут
echo   - TELEGRAM_BOT_GUIDE.md - Полное руководство по боту
echo   - CONSOLIDATED_STARTUP.md - Описание компонентов
echo.
echo ============================================================================
echo.
echo Нажмите любую клавишу для выхода из этого окна...
echo (Компоненты продолжат работать в своих окнах)
pause > nul
endlocal