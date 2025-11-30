# Academy Module — система обучения
# Версия 1.0
#
# Экспорт роутеров модулей Academy

from .v1.module_f3_router import router as router
from .v1.module_f3_router import router_noversion

__all__ = ['router', 'router_noversion']
