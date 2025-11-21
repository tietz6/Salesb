
from fastapi import APIRouter, Request
from .service import list_scenarios, random_scenario, rubric

router = APIRouter(prefix="/trainer_scenarios/v1", tags=["trainer_scenarios"])
router_noversion = APIRouter(prefix="/trainer_scenarios", tags=["trainer_scenarios"])

@router.post("/start")
async def start_telegram(req: Request):
    """Telegram bot integration endpoint - accepts chat_id"""
    data = await req.json()
    probe = data.get("probe", False)
    
    # Quick response for probe requests (discovery)
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Trainer Scenarios module - use /list, /random, /rubric endpoints"}

@router.post("/start_session")
async def start_session(req: Request):
    """Session start endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Trainer Scenarios module - use /list, /random, /rubric endpoints"}

@router.post("/run")
async def run(req: Request):
    """Run endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Trainer Scenarios module - use /list, /random, /rubric endpoints"}

@router.post("/init")
async def init(req: Request):
    """Init endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Trainer Scenarios module - use /list, /random, /rubric endpoints"}

@router.get("/list")
async def ls():
    return list_scenarios()

@router.get("/random")
async def rnd():
    return random_scenario()

@router.get("/rubric")
async def rb():
    return rubric()

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

@router_noversion.get("/list")
async def ls_noversion():
    return await ls()

@router_noversion.get("/random")
async def rnd_noversion():
    return await rnd()

@router_noversion.get("/rubric")
async def rb_noversion():
    return await rb()
