# Consolidated Startup Guide

## Изменения

### Что изменилось?

Теперь **все необходимые компоненты системы** запускаются одним файлом `start_core_api.bat`.

### До изменений

Ранее требовалось запускать компоненты отдельно, что приводило к конфликтам:
- `start_core_api.bat` - для API и части ботов
- `start_telegram_bot.bat` - для основного Telegram бота
- main.py и uvicorn конфликтовали на порту 8080
- simple_telegram_bot.py и telegram_bot.py конфликтовали (один токен)

### После изменений

Теперь достаточно запустить только:
```cmd
start_core_api.bat
```

## Что запускается?

При запуске `start_core_api.bat` автоматически стартуют **2 компонента** в отдельных окнах:

1. **SALESBOT_API** - FastAPI сервер на порту 8080 (через uvicorn)
2. **SALESBOT_TELEGRAM_BOT** - Полнофункциональный Telegram бот с aiogram 3.x и всеми модулями тренировки

### Почему не 4 компонента?

**Удалённые компоненты (из-за конфликтов):**
- ❌ **main.py** - Конфликтовал с uvicorn (оба на порту 8080). Теперь используется только uvicorn.
- ❌ **simple_telegram_bot.py** - Конфликтовал с telegram_bot.py (оба использовали один токен). Теперь используется только telegram_bot.py с полным функционалом.

**Альтернативный запуск:**
Если вам нужен simple_telegram_bot.py (упрощённый API-based бот), используйте отдельный скрипт:
```cmd
start_simple_telegram_bot.bat
```
⚠️ **ВАЖНО:** Не запускайте оба бота одновременно с одним токеном!

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

После запуска проверьте, что оба окна открылись:
- **Окно SALESBOT_API** - FastAPI сервер (должен отображаться uvicorn на порту 8080)
- **Окно SALESBOT_TELEGRAM_BOT** - Telegram бот (должно показать "[telegram_bot] Bot is running!")

### Признаки успешного запуска:

**В окне SALESBOT_API:**
```
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080
```

**В окне SALESBOT_TELEGRAM_BOT:**
```
[telegram_bot] Registering main menu and commands...
[telegram_bot] Auto-loading module handlers...
[tg_autoload] Registered telegram handlers for modules.arena
[tg_autoload] Registered telegram handlers for modules.deepseek_persona
[tg_autoload] Registered telegram handlers for modules.master_path
[tg_autoload] Registered telegram handlers for modules.objections
[tg_autoload] Registered telegram handlers for modules.upsell
[telegram_bot] Bot is running! Connected to Telegram API.
```

## Остановка

Чтобы остановить все компоненты, просто закройте все открытые окна или нажмите Ctrl+C в каждом окне.

## Поддержка

Для получения дополнительной информации см.:
- `QUICK_START.md` - Быстрое руководство по началу работы
- `TELEGRAM_COMPLETE_GUIDE.md` - Полное руководство по Telegram боту
- `README_CORE.txt` - Информация об API
