from fastapi import FastAPI
import importlib
ROUTE_MODULES = [
    # Публичные API
    "api.voice.v1.routes",

    # Основные модули тренажёра
    "api.modules.master_path.v3.routes",
    "api.modules.objections.v3.routes",
    "api.modules.upsell.v3.routes",
    "api.modules.arena.v4.routes",
    "api.modules.sleeping_dragon.v4.routes",
    "api.modules.exam_autocheck.v2.routes",
    "api.modules.payments.v2.routes",

    # Trainer-пакет (новые модули)
    "api.modules.trainer_core.v1.routes",
    "api.modules.trainer_scenarios.v1.routes",
    "api.modules.trainer_dialog_engine.v1.routes",
    "api.modules.trainer_arena_pro.v1.routes",
    "api.modules.trainer_upsell_master.v1.routes",
    "api.modules.trainer_story_collection.v1.routes",
    "api.modules.trainer_exam.v1.routes",

    # Доп-модули
    "api.modules.voice_arena.v1.routes",
    "api.modules.dialog_memory.v1.routes",
    "api.modules.edu_lessons.v1.routes",
    "api.modules.client_cases.v1.routes",

    # Интеграции
    "integrations.telegram_push.v1.routes",
    "integrations.telegram_bot.v1.routes",
]
def include_all(app: FastAPI)->None:
    attached = []
    errors = []
    for m in ROUTE_MODULES:
        try:
            mod = importlib.import_module(m)
            router = getattr(mod, "router", None)
            if router is None:
                continue
            app.include_router(router)
            attached.append(m)
        except Exception as e:
            errors.append((m, str(e)))

    @app.get("/api/public/v1/routes_summary")
    async def routes_summary():
        return {"attached": attached, "errors": errors}
