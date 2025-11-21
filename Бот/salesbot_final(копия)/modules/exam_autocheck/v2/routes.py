from fastapi import APIRouter, Request
from .engine import ExamAutoCheck

# Main router with /exam/v2 prefix
router = APIRouter(prefix="/exam/v2", tags=["exam"])

# Additional router with /exam_autocheck/v2 prefix for compatibility
router_autocheck = APIRouter(prefix="/exam_autocheck/v2", tags=["exam_autocheck"])

# Additional router with /exam_autocheck prefix (no version) for compatibility
router_autocheck_noversion = APIRouter(prefix="/exam_autocheck", tags=["exam_autocheck"])

@router.post("/start")
async def start_telegram(req: Request):
    """Telegram bot integration endpoint - accepts chat_id"""
    data = await req.json()
    chat_id = data.get("chat_id")
    probe = data.get("probe", False)
    
    # Quick response for probe requests (discovery)
    if probe:
        return {"ok": True, "available": True}
    
    if not chat_id:
        return {"error": "chat_id required"}
    
    # Use chat_id as session ID for telegram users
    sid = str(chat_id)
    ex = ExamAutoCheck(sid)
    result = ex.start()
    
    return {
        "ok": True,
        "sid": sid,
        "reply": f"📝 Автоматическая проверка экзамена!\n\n"
                 f"Модуль: {result['module']}\n\n"
                 f"Я буду задавать вопросы и оценивать твои ответы.\n"
                 f"Всего 5 вопросов. Начнём!"
    }

@router.post("/start/{sid}")
async def start(sid:str):
    ex = ExamAutoCheck(sid)
    result = ex.start()
    return {"ok": True, "sid": sid}

@router.post("/start_session")
async def start_session(req: Request):
    """Session start endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Use /start endpoint"}

@router.post("/run")
async def run(req: Request):
    """Run endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Use /start endpoint"}

@router.post("/init")
async def init(req: Request):
    """Init endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Use /start endpoint"}

# Duplicate endpoints for /exam_autocheck/v2 prefix
@router_autocheck.post("/start")
async def start_telegram_autocheck(req: Request):
    return await start_telegram(req)

@router_autocheck.post("/start/{sid}")
async def start_autocheck(sid: str):
    return await start(sid)

@router_autocheck.post("/start_session")
async def start_session_autocheck(req: Request):
    return await start_session(req)

@router_autocheck.post("/run")
async def run_autocheck(req: Request):
    return await run(req)

@router_autocheck.post("/init")
async def init_autocheck(req: Request):
    return await init(req)

# Duplicate endpoints for /exam_autocheck prefix (no version)
@router_autocheck_noversion.post("/start")
async def start_telegram_noversion(req: Request):
    return await start_telegram(req)

@router_autocheck_noversion.post("/start/{sid}")
async def start_noversion(sid: str):
    return await start(sid)

@router_autocheck_noversion.post("/start_session")
async def start_session_noversion(req: Request):
    return await start_session(req)

@router_autocheck_noversion.post("/run")
async def run_noversion(req: Request):
    return await run(req)

@router_autocheck_noversion.post("/init")
async def init_noversion(req: Request):
    return await init(req)