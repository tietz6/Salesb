# Руководство по решению проблем с Telegram ботом

## Проблема: Бот не подключается к Telegram

### Симптомы
- Ошибка: `Cannot connect to host api.telegram.org`
- Ошибка: `No address associated with hostname`
- Ошибка: `TelegramNetworkError`
- Бот не отвечает на команды

### Диагностика

Запустите скрипт диагностики:
```bash
python test_telegram_connection.py
```

Этот скрипт проверит:
- ✅ Наличие токена
- ✅ Установлен ли aiogram
- ✅ Доступ к Telegram API
- ✅ Информацию о боте

---

## Решения

### Решение 1: Проверка токена

**Если ошибка:** `Unauthorized` или `Invalid token`

1. Получите новый токен от [@BotFather](https://t.me/BotFather):
   - Отправьте `/newbot` или `/token`
   - Скопируйте новый токен

2. Обновите токен в файле `start_core_api.bat`:
   ```batch
   set TELEGRAM_TOKEN=ВАШ_НОВЫЙ_ТОКЕН
   set TELEGRAM_BOT_TOKEN=ВАШ_НОВЫЙ_ТОКЕН
   set TG_BOT_TOKEN=ВАШ_НОВЫЙ_ТОКЕН
   ```

3. Перезапустите бота

---

### Решение 2: Проверка интернет-соединения

**Если ошибка:** `Cannot connect to host` или `DNS resolution`

1. Проверьте доступ к интернету:
   ```bash
   ping 8.8.8.8
   curl https://www.google.com
   ```

2. Проверьте доступ к Telegram:
   ```bash
   curl https://api.telegram.org
   nslookup api.telegram.org
   ```

3. Если Telegram заблокирован, используйте Решение 3 или 4

---

### Решение 3: Использование прокси

**Если Telegram API заблокирован в вашей сети**

#### Вариант A: HTTP/HTTPS прокси

1. Установите дополнительные зависимости:
   ```bash
   pip install aiohttp-socks
   ```

2. Создайте файл `telegram_bot_proxy.py`:
   ```python
   import os
   import asyncio
   from aiogram import Bot, Dispatcher
   from aiohttp_socks import ProxyConnector
   from aiogram.client.session.aiohttp import AiohttpSession
   
   # Настройка прокси
   PROXY_URL = "socks5://user:password@proxy-host:1080"  # или http://proxy:8080
   
   connector = ProxyConnector.from_url(PROXY_URL)
   session = AiohttpSession(connector=connector)
   
   TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
   bot = Bot(token=TELEGRAM_TOKEN, session=session)
   # ... rest of the code
   ```

3. Запустите бота:
   ```bash
   python telegram_bot_proxy.py
   ```

#### Вариант B: Использование переменных окружения

1. Установите прокси через переменные окружения:
   ```bash
   set HTTP_PROXY=http://proxy-server:8080
   set HTTPS_PROXY=http://proxy-server:8080
   ```

2. Запустите бота как обычно

---

### Решение 4: Локальный Bot API Server

**Рекомендуется для продакшена или при блокировке Telegram**

Telegram предоставляет возможность запустить собственный Bot API Server:

1. Скачайте Bot API Server:
   - Репозиторий: https://github.com/tdlib/telegram-bot-api
   - Или используйте Docker:
     ```bash
     docker run -d -p 8081:8081 --name telegram-bot-api \
       -e TELEGRAM_API_ID=YOUR_API_ID \
       -e TELEGRAM_API_HASH=YOUR_API_HASH \
       aiogram/telegram-bot-api
     ```

2. Настройте бота для использования локального сервера:
   
   В `start_core_api.bat` добавьте:
   ```batch
   set TELEGRAM_API_SERVER=http://localhost:8081
   ```
   
   Или в командной строке:
   ```bash
   export TELEGRAM_API_SERVER=http://localhost:8081
   python telegram_bot.py
   ```

3. Бот автоматически будет использовать локальный сервер

**Преимущества:**
- ✅ Нет проблем с блокировкой
- ✅ Больше контроля
- ✅ Можно скачивать большие файлы
- ✅ Работает в любой сети

---

### Решение 5: Режим Webhook (альтернатива polling)

**Если polling не работает, используйте webhook**

Создайте файл `telegram_webhook.py`:
```python
import os
from aiogram import Bot, Dispatcher
from fastapi import FastAPI, Request
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = "https://your-domain.com/webhook"  # Ваш публичный URL

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Регистрация хэндлеров
# ... (код регистрации как в telegram_bot.py)

async def on_startup(bot: Bot):
    await bot.set_webhook(f"{WEBHOOK_URL}/bot{TELEGRAM_TOKEN}")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()

def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=f"/bot{TELEGRAM_TOKEN}")
    setup_application(app, dp, bot=bot)
    
    web.run_app(app, host="0.0.0.0", port=8443)

if __name__ == "__main__":
    main()
```

**Требования для webhook:**
- HTTPS-сертификат
- Публичный IP или домен
- Открытый порт (443, 80, 88, или 8443)

---

### Решение 6: Использование ngrok (для тестирования webhook)

1. Установите ngrok: https://ngrok.com/download

2. Запустите ngrok:
   ```bash
   ngrok http 8080
   ```

3. Скопируйте HTTPS URL (например: `https://abc123.ngrok.io`)

4. Установите переменную окружения:
   ```bash
   set WEBHOOK_URL=https://abc123.ngrok.io
   ```

5. Запустите бота в режиме webhook

---

## Проверка после исправления

После применения любого из решений, проверьте работу бота:

1. Запустите диагностику:
   ```bash
   python test_telegram_connection.py
   ```

2. Если тест успешен, запустите бота:
   ```bash
   python telegram_bot.py
   ```
   
   Или полную систему:
   ```bash
   start_core_api.bat
   ```

3. Откройте Telegram и отправьте боту команду `/start`

4. Вы должны получить приветственное сообщение с меню

---

## Дополнительная помощь

### Логи и отладка

Для получения подробных логов:
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Проверка статуса бота

Онлайн-проверка токена:
```bash
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

### Полезные ссылки

- [Официальная документация Telegram Bot API](https://core.telegram.org/bots/api)
- [Aiogram документация](https://docs.aiogram.dev/)
- [Telegram Bot API Server](https://github.com/tdlib/telegram-bot-api)
- [Список прокси-серверов](https://www.freeproxy.world/)

---

## Частые вопросы

**Q: Можно ли запустить бота без интернета?**  
A: Нет, бот должен быть подключен к Telegram API. Но можно использовать локальный Bot API Server с кешированием.

**Q: Как узнать, заблокирован ли Telegram в моей сети?**  
A: Выполните: `nslookup api.telegram.org` и `curl https://api.telegram.org`. Если команды не работают, Telegram заблокирован.

**Q: Безопасно ли использовать прокси?**  
A: Используйте только доверенные прокси. Лучше настроить собственный Bot API Server.

**Q: Почему бот работал раньше, а сейчас нет?**  
A: Возможные причины:
- Токен был отозван (проверьте у @BotFather)
- Изменились настройки сети/firewall
- Telegram API временно недоступен (проверьте статус: https://www.githubstatus.com/)

---

## Поддержка

Если ни одно из решений не помогло:

1. Запустите диагностику и сохраните вывод:
   ```bash
   python test_telegram_connection.py > diagnosis.txt
   ```

2. Проверьте логи бота

3. Обратитесь за помощью с информацией:
   - Версия Python (`python --version`)
   - Версия aiogram (`pip show aiogram`)
   - Операционная система
   - Результаты диагностики
   - Текст ошибки

---

**Последнее обновление:** 2025-11-21  
**Версия:** 1.0
