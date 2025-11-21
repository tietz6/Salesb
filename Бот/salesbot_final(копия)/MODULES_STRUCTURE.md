# Modules Structure Guide

## Module Versioning Pattern

Each module in the `modules/` directory follows a versioned structure:

```
modules/
├── module_name/
│   ├── __init__.py           # Optional: Top-level exports for Telegram integration
│   ├── v1/                   # Version 1 (deprecated)
│   ├── v2/                   # Version 2 (deprecated)
│   ├── v3/                   # Version 3 (current active version)
│   │   ├── __init__.py
│   │   ├── engine.py         # Business logic
│   │   ├── routes.py         # FastAPI routes
│   │   └── README_INSTALL.txt
│   └── _current/             # Legacy alias (may contain integration helpers)
│       ├── __init__.py
│       ├── engine.py
│       ├── routes.py
│       └── glue_*.py         # Integration helpers (optional)
```

## Active Versions (used by FastAPI)

The `router_autoload.py` file explicitly specifies which version of each module to load:

| Module | Active Version | Route Prefix |
|--------|---------------|--------------|
| master_path | v3 | /master_path/v3 |
| objections | v3 | /objections/v3 |
| upsell | v3 | /upsell/v3 |
| arena | v4 | /arena/v4 |
| sleeping_dragon | v4 | /sleeping_dragon/v4 |
| exam_autocheck | v2 | /exam/v2 |
| trainer_core | v1 | /trainer_core/v1 |
| trainer_scenarios | v1 | /trainer_scenarios/v1 |
| trainer_dialog_engine | v1 | /trainer_dialog_engine/v1 |
| trainer_arena_pro | v1 | /trainer_arena_pro/v1 |
| trainer_upsell_master | v1 | /trainer_upsell_master/v1 |
| trainer_story_collection | v1 | /trainer_story_collection/v1 |
| trainer_exam | v1 | /trainer_exam/v1 |
| voice_arena | v1 | /voice_arena/v1 |
| dialog_memory | v1 | /dialog_memory/v1 |
| edu_lessons | v1 | /edu_lessons/v1 |
| client_cases | v1 | /client_cases/v1 |

## `_current` Directories

### Purpose
The `_current` directories were originally designed as a stable alias for the current production version. However, in practice:

1. **Not used by FastAPI**: The `router_autoload.py` explicitly imports versioned modules (v1, v2, v3, v4)
2. **Partially used by Telegram**: Only `deepseek_persona/__init__.py` tries to import from `_current`
3. **Contains extras**: Many `_current` directories include additional "glue" files not present in the versioned directories

### Glue Files

Glue files are integration helpers that bridge modules together:

- `glue_pricing.py` - Price calculation helpers (in upsell/_current)
- `glue_rubrics.py` - Scoring helpers (in master_path/_current)
- `glue_psychotypes.py` - Personality helpers (in arena/_current)
- `glue_classifier.py` - Classification helpers (in objections/_current)
- `glue_rules.py` - Rule-based helpers (in sleeping_dragon/_current)

**Status**: These glue files are currently NOT imported by any active code but remain available for future integration.

### Should You Delete `_current`?

**No** - Keep them for these reasons:
1. They contain additional integration code (glue files) not in versioned directories
2. `deepseek_persona` actively tries to use `_current` for Telegram integration
3. They serve as a backup/reference for the latest stable version
4. They don't interfere with the current system (versioned imports are explicit)
5. May be useful for future development or migration

### Recommendation

If you want to clean up:
1. Migrate useful glue files from `_current` into the appropriate versioned directories
2. Update `deepseek_persona/__init__.py` to import from v1 directly
3. Then safely remove all `_current` directories

But for now, **leaving them causes no harm** and keeps options open.

## Module Registration

### For FastAPI (REST API)

Add module route to `router_autoload.py`:

```python
ROUTE_MODULES = [
    "modules.your_module.v1.routes",  # Add your module here
    # ...
]
```

Your `routes.py` should export a router:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/your_module/v1", tags=["your_module"])

@router.get("/endpoint")
async def handler():
    return {"ok": True}
```

### For Telegram Bot

Create a `register_telegram` function in your module's `__init__.py`:

```python
def register_telegram(dp, registry):
    """
    Register Telegram handlers for this module.
    
    Args:
        dp: aiogram Dispatcher
        registry: ModuleRegistry instance
    """
    from aiogram import types
    from aiogram.filters import Command
    
    @dp.message(Command("your_command"))
    async def handler(message: types.Message):
        await message.answer("Response")
```

The `telegram/autoload.py` will automatically discover and register it.

## Best Practices

1. **Version explicitly**: Don't rely on `_current` - specify version in imports
2. **One active version**: Only one version per module should be in `ROUTE_MODULES`
3. **Keep old versions**: Useful for comparison and rollback if needed
4. **Document changes**: Update this file when adding/upgrading modules
5. **Test both interfaces**: Ensure module works in both FastAPI and Telegram bot

## Migration Between Versions

If you're upgrading a module from v3 to v4:

1. Copy `modules/your_module/v3/` to `modules/your_module/v4/`
2. Make your changes in v4
3. Test thoroughly
4. Update `router_autoload.py`:
   ```python
   # Old:
   "modules.your_module.v3.routes",
   # New:
   "modules.your_module.v4.routes",
   ```
5. Restart both FastAPI and Telegram bot
6. Keep v3 around for a few releases as backup

## Common Issues

### Issue: Module not loading in FastAPI
**Solution**: Check if it's listed in `ROUTE_MODULES` in `router_autoload.py`

### Issue: Module not responding in Telegram
**Solution**: Ensure `register_telegram()` function exists in module's `__init__.py`

### Issue: Import errors
**Solution**: Use absolute imports: `from modules.your_module.v1.engine import ...`

### Issue: Route conflicts
**Solution**: Each module version must have a unique prefix: `/your_module/v1`, `/your_module/v2`, etc.
