@echo off
setlocal

REM --- переходим в папку с проектом ---
cd /d "%~dp0"

REM --- активируем виртуальное окружение ---
call venv\Scripts\activate

REM === КЛЮЧИ И НАСТРОЙКИ ===

REM DeepSeek
set DEEPSEEK_API_KEY=sk-4de54b0041b44cf193b22cf21f028be7
set DEEPSEEK_MODEL=deepseek-chat
REM Можно не задавать, у нас в коде есть значение по умолчанию,
REM но если хочешь явно:
REM set DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions

REM Голос (ASR)
set VOICE_API_KEY=10da831f2d514801a47c79b8e3e68ebb

REM Телеграм-бот для пушей
REM === ТЕЛЕГРАМ ДЛЯ PUSH ===
set TELEGRAM_BOT_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI
set TG_BOT_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI
set TELEGRAM_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI
set TELEGRAM_PUSH_MOCK_MODE=false

echo ===================================
echo SALESBOT - Запуск всех компонентов
echo ===================================
echo.
echo Telegram Bot Token: %TELEGRAM_BOT_TOKEN%
echo DeepSeek API Key: %DEEPSEEK_API_KEY%
echo Voice API Key: %VOICE_API_KEY%
echo.

REM === ЗАПУСК API ===
echo [1/2] Запуск FastAPI сервера...
start "SALESBOT_API" python -m uvicorn startup:app --host 0.0.0.0 --port 8080 --reload

REM Пауза для запуска сервера
timeout /t 3 /nobreak > nul

REM === Запускаем telegram_bot.py (основной бот с aiogram 3.x) ===
echo [2/2] Запуск Telegram бота с модулями...
start "SALESBOT_TELEGRAM_BOT" python telegram_bot.py

echo.
echo ===================================
echo Все компоненты запущены!
echo ===================================
echo.
echo Открытые окна:
echo - SALESBOT_API: FastAPI сервер (порт 8080)
echo - SALESBOT_TELEGRAM_BOT: Telegram бот с модулями тренировки
echo.
echo Доступные команды в боте:
echo   /start или /menu - Главное меню
echo   /master_path - Путь Мастера (полный цикл продажи)
echo   /arena - Арена с AI-клиентами
echo   /objections - Работа с возражениями
echo   /upsell - Допродажи
echo   /coach ^<вопрос^> - Совет коуча
echo   /stylize ^<текст^> - Стилизация под бренд
echo   /products - Каталог продуктов
echo   /script - Скрипт продаж
echo   /stats - Статистика тренировок
echo.
echo Нажмите любую клавишу для выхода...
pause
endlocal