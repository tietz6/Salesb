#!/bin/bash
# Скрипт проверки установки модуля F3 — Эмоциональная коммуникация
# Запуск: bash scripts/check_f3_install.sh

set -e

echo "=== Проверка модуля F3 — Эмоциональная коммуникация ==="
echo ""

# Переходим в корневую папку проекта
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "1. Проверка синтаксиса module_f3_service.py..."
python -m py_compile modules/academy/v1/module_f3_service.py
echo "   ✓ OK"

echo ""
echo "2. Проверка синтаксиса module_f3_router.py..."
python -m py_compile modules/academy/v1/module_f3_router.py
echo "   ✓ OK"

echo ""
echo "3. Проверка синтаксиса module_f3_emotion.py..."
python -m py_compile modules/academy/v1/module_f3_emotion.py
echo "   ✓ OK"

echo ""
echo "4. Проверка импорта get_module..."
python -c "from modules.academy.v1.module_f3_service import get_module; print('   Module ID:', get_module()['id'])"
echo "   ✓ OK"

echo ""
echo "5. Проверка импорта роутера..."
python -c "from modules.academy.v1.module_f3_router import router; print('   Router prefix:', router.prefix)"
echo "   ✓ OK"

echo ""
echo "6. Проверка импорта из academy..."
python -c "from modules.academy import router; print('   Academy router:', router.prefix)"
echo "   ✓ OK"

echo ""
echo "=== Все проверки пройдены успешно! ==="
echo ""
echo "Для полного тестирования запустите сервер:"
echo "  python main.py"
echo ""
echo "И проверьте эндпоинты:"
echo "  curl http://127.0.0.1:8080/academy/v1/modules/module_f3/"
echo "  curl http://127.0.0.1:8080/academy/v1/modules/module_f3/lessons/lesson_1"
