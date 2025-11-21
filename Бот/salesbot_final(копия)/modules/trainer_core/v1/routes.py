
from fastapi import APIRouter, Request
from .service import evaluate

router = APIRouter(prefix="/trainer_core/v1", tags=["trainer_core"])
router_noversion = APIRouter(prefix="/trainer_core", tags=["trainer_core"])

@router.post("/start")
async def start_telegram(req: Request):
    """Telegram bot integration endpoint - accepts chat_id"""
    data = await req.json()
    probe = data.get("probe", False)
    
    # Quick response for probe requests (discovery)
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Trainer Core module - use /evaluate endpoint"}

@router.post("/start_session")
async def start_session(req: Request):
    """Session start endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Trainer Core module - use /evaluate endpoint"}

@router.post("/run")
async def run(req: Request):
    """Run endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Trainer Core module - use /evaluate endpoint"}

@router.post("/init")
async def init(req: Request):
    """Init endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Trainer Core module - use /evaluate endpoint"}

@router.post("/evaluate")
async def ev(req: Request):
    data = await req.json()
    text = data.get("text","")
    return evaluate(text)

# Non-versioned endpoints
@router_noversion.post("/start")
async def start_telegram_noversion(req: Request):
    return await start_telegram(req)

@router_noversion.post("/start_session")
async def start_session_noversion(req: Request):
    return await start_session(req)

@router_noversion.post("/run")
async def run_noversion(req: Request):
    return await run(req)

@router_noversion.post("/init")
async def init_noversion(req: Request):
    return await init(req)

@router_noversion.post("/evaluate")
async def ev_noversion(req: Request):
    return await ev(req)
