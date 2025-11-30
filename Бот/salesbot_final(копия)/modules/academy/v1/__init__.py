# Academy Module v1 — Система обучения
# Версия 1.0
#
# Экспорт роутеров модулей Academy

from .module_f3_router import router as module_f3_router
from .module_f3_router import router_noversion as module_f3_router_noversion

__all__ = ['module_f3_router', 'module_f3_router_noversion']
