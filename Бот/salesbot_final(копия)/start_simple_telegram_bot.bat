@echo off
setlocal

REM ============================================================================
REM SALESBOT - Simple Telegram Bot Startup
REM ============================================================================
REM Этот скрипт запускает упрощённый Telegram бот (simple_telegram_bot.py)
REM который работает через HTTP API с backend сервером.
REM
REM ВАЖНО: 
REM 1. Backend сервер (FastAPI) должен быть запущен ПЕРЕД этим ботом
REM 2. НЕ запускайте этот бот одновременно с telegram_bot.py - будет конфликт!
REM 3. Оба бота не могут работать с одним токеном одновременно
REM
REM Когда использовать simple_telegram_bot.py:
REM - Вы хотите более простой, API-based подход
REM - Вам нужна базовая функциональность без aiogram
REM - Вы разрабатываете новые модули и тестируете их через HTTP API
REM
REM Когда использовать telegram_bot.py:
REM - Вам нужен полный функционал с интерактивным меню
REM - Вы хотите использовать все модули тренировки
REM - Рекомендуется для продакшн использования
REM ============================================================================

REM --- переходим в папку с проектом ---
cd /d "%~dp0"

REM --- активируем виртуальное окружение ---
echo Активация виртуального окружения...
call venv\Scripts\activate
if errorlevel 1 (
    echo ОШИБКА: Не удалось активировать виртуальное окружение venv
    echo Убедитесь, что папка venv существует и содержит правильное окружение
    pause
    exit /b 1
)

REM ============================================================================
REM === НАСТРОЙКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ===
REM ============================================================================

REM === Telegram Bot Token ===
set TELEGRAM_BOT_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI
set TG_BOT_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI
set TELEGRAM_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI

REM === Backend URL ===
set BACKEND_URL=http://127.0.0.1:8080

REM === DeepSeek AI (опционально для некоторых модулей) ===
set DEEPSEEK_API_KEY=sk-4de54b0041b44cf193b22cf21f028be7
set DEEPSEEK_MODEL=deepseek-chat

REM ============================================================================
REM === ПРОВЕРКА BACKEND СЕРВЕРА ===
REM ============================================================================

echo.
echo ============================================================================
echo            SALESBOT - Запуск Simple Telegram Bot
echo ============================================================================
echo.
echo Конфигурация:
echo   Telegram Bot Token: %TELEGRAM_BOT_TOKEN%
echo   Backend URL: %BACKEND_URL%
echo.
echo ВАЖНО: Backend сервер должен быть запущен!
echo.
echo Проверка доступности backend сервера...

REM Проверяем доступность backend через curl или PowerShell
powershell -Command "try { $r = Invoke-WebRequest -Uri '%BACKEND_URL%/api/public/v1/health' -TimeoutSec 5; if ($r.StatusCode -eq 200) { Write-Host 'Backend сервер доступен!' -ForegroundColor Green; exit 0 } else { Write-Host 'Backend сервер не отвечает!' -ForegroundColor Red; exit 1 } } catch { Write-Host 'Backend сервер недоступен!' -ForegroundColor Red; Write-Host 'Сначала запустите: start_core_api.bat' -ForegroundColor Yellow; exit 1 }"

if errorlevel 1 (
    echo.
    echo ОШИБКА: Backend сервер недоступен по адресу %BACKEND_URL%
    echo.
    echo Пожалуйста, сначала запустите backend сервер:
    echo   1. Откройте новое окно командной строки
    echo   2. Перейдите в папку проекта
    echo   3. Запустите: python -m uvicorn startup:app --host 0.0.0.0 --port 8080
    echo.
    echo Или используйте полный запуск через start_core_api.bat
    echo.
    pause
    exit /b 1
)

REM ============================================================================
REM === ЗАПУСК SIMPLE TELEGRAM BOT ===
REM ============================================================================

echo.
echo ============================================================================
echo.
echo Запуск Simple Telegram Bot...
echo Бот будет работать через HTTP API с backend сервером.
echo.
echo Доступные команды:
echo   /start - Показать доступные команды
echo   /train или /dialog - Начать тренировку
echo   /stop_dialog - Остановить текущую сессию
echo   /modules - Показать доступные модули
echo.
echo ============================================================================
echo.

REM Запускаем бота
python simple_telegram_bot.py

REM Если бот завершился
echo.
echo ============================================================================
echo Simple Telegram Bot остановлен
echo ============================================================================
echo.
pause
endlocal
