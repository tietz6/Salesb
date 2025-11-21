# Consolidated Startup Guide

## Изменения

### Что изменилось?

Теперь **все компоненты системы** запускаются одним файлом `start_core_api.bat`.

### До изменений

Ранее требовалось запускать компоненты отдельно:
- `start_core_api.bat` - для API и части ботов
- `start_telegram_bot.bat` - для основного Telegram бота

### После изменений

Теперь достаточно запустить только:
```cmd
start_core_api.bat
```

## Что запускается?

При запуске `start_core_api.bat` автоматически стартуют 4 компонента в отдельных окнах:

1. **SALESBOT_API** - FastAPI сервер на порту 8080
2. **SALESBOT_MAIN** - Основное приложение (main.py)
3. **SALESBOT_SIMPLE_BOT** - Простой Telegram бот (simple_telegram_bot.py)
4. **SALESBOT_TELEGRAM_BOT** - Продвинутый Telegram бот с модулями (telegram_bot.py)

## Настройка переменных окружения

Все необходимые переменные окружения установлены в `start_core_api.bat`:

```batch
REM DeepSeek API
set DEEPSEEK_API_KEY=sk-4de54b0041b44cf193b22cf21f028be7
set DEEPSEEK_MODEL=deepseek-chat

REM Voice API
set VOICE_API_KEY=10da831f2d514801a47c79b8e3e68ebb

REM Telegram Bot
set TELEGRAM_BOT_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI
set TG_BOT_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI
set TELEGRAM_TOKEN=8029409301:AAGpKsSxQ_rdQJm_5kR6hk_E5JgOoQLNAgI
set TELEGRAM_PUSH_MOCK_MODE=false
```

## Быстрый старт

1. Убедитесь, что Python и виртуальное окружение установлены
2. Откройте `start_core_api.bat`
3. При необходимости замените токены на свои
4. Запустите файл двойным щелчком или из командной строки

## Устаревшие файлы

- `start_telegram_bot.bat` - теперь показывает предупреждение об устаревании
- `start_telegram_bot.bat.deprecated` - резервная копия старого файла

## Проверка работы

После запуска проверьте, что все окна открылись:
- Окно с FastAPI (должен отображаться uvicorn)
- Окно с main.py
- Окно с simple_telegram_bot.py
- Окно с telegram_bot.py (должно показать "[telegram_bot] Bot is running!")

## Остановка

Чтобы остановить все компоненты, просто закройте все открытые окна или нажмите Ctrl+C в каждом окне.

## Поддержка

Для получения дополнительной информации см.:
- `QUICK_START.md` - Быстрое руководство по началу работы
- `TELEGRAM_COMPLETE_GUIDE.md` - Полное руководство по Telegram боту
- `README_CORE.txt` - Информация об API
