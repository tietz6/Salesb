@echo off
setlocal

REM ============================================================================
REM TELEGRAM BOT STARTUP SCRIPT - Multiple modes available
REM ============================================================================

cd /d "%~dp0"

REM Activate virtual environment if exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate
)

REM === Установка переменных окружения ===
set TELEGRAM_BOT_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI
set TELEGRAM_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI
set TG_BOT_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI
set DEEPSEEK_API_KEY=sk-4de54b0041b44cf193b22cf21f028be7
set VOICE_API_KEY=10da831f2d514801a47c79b8e3e68ebb

echo.
echo ============================================================================
echo                      TELEGRAM BOT STARTUP MENU
echo ============================================================================
echo.
echo Выберите режим запуска:
echo.
echo   1 - Диагностика подключения (проверить токен и доступ к Telegram)
echo   2 - Запуск в режиме Polling (стандартный режим)
echo   3 - Запуск в режиме Webhook (альтернативный режим)
echo   4 - Запуск с пользовательским API сервером
echo   5 - Показать справку по решению проблем
echo   0 - Выход
echo.
echo ============================================================================
echo.

set /p choice="Введите номер (0-5): "

if "%choice%"=="1" goto diagnostic
if "%choice%"=="2" goto polling
if "%choice%"=="3" goto webhook
if "%choice%"=="4" goto custom_api
if "%choice%"=="5" goto help
if "%choice%"=="0" goto end

echo Неверный выбор!
pause
goto end

:diagnostic
echo.
echo ============================================================================
echo Запуск диагностики подключения...
echo ============================================================================
echo.
python test_telegram_connection.py
echo.
echo Нажмите любую клавишу для возврата в меню...
pause > nul
goto end

:polling
echo.
echo ============================================================================
echo Запуск бота в режиме Polling...
echo ============================================================================
echo.
echo Этот режим использует long polling для получения обновлений.
echo Требуется постоянное подключение к api.telegram.org
echo.
python telegram_bot.py
pause
goto end

:webhook
echo.
echo ============================================================================
echo Запуск бота в режиме Webhook...
echo ============================================================================
echo.
echo ВНИМАНИЕ: Для работы webhook требуется:
echo   - Публичный HTTPS URL (можно использовать ngrok для тестирования)
echo   - Открытый порт (по умолчанию 8443)
echo.
set /p webhook_url="Введите URL webhook (или нажмите Enter для localhost): "
if "%webhook_url%"=="" set webhook_url=https://localhost:8443

echo.
echo Установка WEBHOOK_URL=%webhook_url%
set WEBHOOK_URL=%webhook_url%

echo.
echo Для тестирования с ngrok:
echo   1. Запустите: ngrok http 8443
echo   2. Скопируйте HTTPS URL из ngrok
echo   3. Перезапустите этот скрипт и введите ngrok URL
echo.
echo Запуск...
python telegram_webhook.py
pause
goto end

:custom_api
echo.
echo ============================================================================
echo Запуск с пользовательским API сервером...
echo ============================================================================
echo.
echo Этот режим позволяет использовать:
echo   - Локальный Telegram Bot API Server
echo   - Прокси-сервер
echo   - Альтернативный API endpoint
echo.
set /p api_server="Введите URL API сервера (например, http://localhost:8081): "

if "%api_server%"=="" (
    echo Ошибка: URL не может быть пустым!
    pause
    goto end
)

echo.
echo Установка TELEGRAM_API_SERVER=%api_server%
set TELEGRAM_API_SERVER=%api_server%

echo Запуск бота...
python telegram_bot.py
pause
goto end

:help
echo.
echo ============================================================================
echo Справка по решению проблем
echo ============================================================================
echo.
type TELEGRAM_TROUBLESHOOTING.md
echo.
echo Для просмотра полной документации откройте файл:
echo   TELEGRAM_TROUBLESHOOTING.md
echo.
pause
goto end

:end
endlocal
