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
echo [1/4] Запуск FastAPI сервера...
start "SALESBOT_API" python -m uvicorn startup:app --host 0.0.0.0 --port 8080 --reload

REM === Запуск main.py ===
echo [2/4] Запуск main.py...
start "SALESBOT_MAIN" python main.py

REM === Запускаем simple_telegram_bot.py ===
echo [3/4] Запуск simple telegram bot...
start "SALESBOT_SIMPLE_BOT" python simple_telegram_bot.py

REM === Запускаем telegram_bot.py (основной бот) ===
echo [4/4] Запуск основного telegram bot...
start "SALESBOT_TELEGRAM_BOT" python telegram_bot.py

echo.
echo ===================================
echo Все компоненты запущены!
echo ===================================
echo.
echo Открытые окна:
echo - SALESBOT_API: FastAPI сервер (порт 8080)
echo - SALESBOT_MAIN: Основное приложение
echo - SALESBOT_SIMPLE_BOT: Простой Telegram бот
echo - SALESBOT_TELEGRAM_BOT: Продвинутый Telegram бот
echo.
echo Нажмите любую клавишу для выхода...
pause
endlocal