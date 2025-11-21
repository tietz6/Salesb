
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
import os

router = APIRouter(prefix="/trainer_arena_pro/v1", tags=["trainer_arena_pro"])
router_noversion = APIRouter(prefix="/trainer_arena_pro", tags=["trainer_arena_pro"])

BASE = os.path.dirname(__file__)
STATIC = os.path.join(BASE,"static")

@router.post("/start")
async def start_telegram(req: Request):
    """Telegram bot integration endpoint - accepts chat_id"""
    data = await req.json()
    probe = data.get("probe", False)
    
    # Quick response for probe requests (discovery)
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Trainer Arena Pro module - use /dashboard endpoint"}

@router.post("/start_session")
async def start_session(req: Request):
    """Session start endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Trainer Arena Pro module - use /dashboard endpoint"}

@router.post("/run")
async def run(req: Request):
    """Run endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Trainer Arena Pro module - use /dashboard endpoint"}

@router.post("/init")
async def init(req: Request):
    """Init endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Trainer Arena Pro module - use /dashboard endpoint"}

@router.get("/static/pro.css")
async def css():
    return FileResponse(os.path.join(STATIC,"pro.css"))

@router.get("/dashboard", response_class=HTMLResponse)
async def dash():
    html = open(os.path.join(BASE,"templates","arena_pro.html"),"r",encoding="utf-8").read()
    # simple render (no jinja here to reduce deps)
    html = html.replace("{{ scenarios }}","7").replace("{{ avg_warmth }}","62").replace("{{ avg_empathy }}","58").replace("{{ avg_questions }}","47")
    return HTMLResponse(html)

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

@router_noversion.get("/static/pro.css")
async def css_noversion():
    return await css()

@router_noversion.get("/dashboard", response_class=HTMLResponse)
async def dash_noversion():
    return await dash()
