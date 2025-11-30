from fastapi import FastAPI
import importlib
import logging

# Configure logger for module loading
log = logging.getLogger("modules.academy.repository")

ROUTE_MODULES = [
    # Публичные API
    # "api.voice.v1.routes",  # Disabled - requires httpx

    # Основные модули тренажёра
    "modules.master_path.v3.routes",
    "modules.objections.v3.routes",
    "modules.upsell.v3.routes",
    "modules.arena.v4.routes",
    "modules.sleeping_dragon.v4.routes",
    "modules.exam_autocheck.v2.routes",
    # "modules.payments.v2.routes",  # Disabled - requires integrations.patch_v4 and bridges.crm_sync

    # Trainer-пакет (новые модули)
    "modules.trainer_core.v1.routes",
    "modules.trainer_scenarios.v1.routes",
    "modules.trainer_dialog_engine.v1.routes",
    "modules.trainer_arena_pro.v1.routes",
    "modules.trainer_upsell_master.v1.routes",
    "modules.trainer_story_collection.v1.routes",
    "modules.trainer_exam.v1.routes",

    # Доп-модули
    "modules.voice_arena.v1.routes",
    "modules.dialog_memory.v1.routes",
    "modules.edu_lessons.v1.routes",
    "modules.client_cases.v1.routes",

    # Academy модули
    "modules.academy.v1.module_f3_router",

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
            
            # Log academy module loading with module info
            if "academy" in m:
                try:
                    # Try to get module data for logging
                    module_f3 = importlib.import_module("modules.academy.v1.module_f3_emotion")
                    module_data = getattr(module_f3, "MODULE_F3_EMOTION", None)
                    if module_data:
                        log.info("Loaded module: %s - %s", module_data.get("id"), module_data.get("title"))
                except Exception:
                    pass
            
            # Also include additional routers if they exist (e.g., router_autocheck, router_autocheck_noversion)
            for attr_name in dir(mod):
                if attr_name.startswith("router_") and attr_name != "router":
                    additional_router = getattr(mod, attr_name, None)
                    if additional_router and hasattr(additional_router, "routes"):
                        app.include_router(additional_router)
                        attached.append(f"{m}.{attr_name}")
        except Exception as e:
            errors.append((m, str(e)))

    @app.get("/api/public/v1/routes_summary")
    async def routes_summary():
        return {"attached": attached, "errors": errors}
