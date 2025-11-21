
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os, json
from .service import list_cases, get_case, top_seller_reply, coach_generate_pitch, arena_context

router = APIRouter(prefix="/client_cases/v1", tags=["client_cases"])
router_noversion = APIRouter(prefix="/client_cases", tags=["client_cases"])

BASE = os.path.dirname(__file__)
TPL = os.path.join(BASE, "templates")
STATIC = os.path.join(BASE, "static")

env = Environment(loader=FileSystemLoader(TPL), autoescape=select_autoescape(["html","xml"]))

@router.post("/start")
async def start_telegram(req: Request):
    """Telegram bot integration endpoint - accepts chat_id"""
    data = await req.json()
    probe = data.get("probe", False)
    
    # Quick response for probe requests (discovery)
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Client Cases module - use /catalog, /list, /get endpoints"}

@router.post("/start_session")
async def start_session_endpoint(req: Request):
    """Session start endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Client Cases module - use /catalog, /list, /get endpoints"}

@router.post("/run")
async def run_endpoint(req: Request):
    """Run endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Client Cases module - use /catalog, /list, /get endpoints"}

@router.post("/init")
async def init_endpoint(req: Request):
    """Init endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Client Cases module - use /catalog, /list, /get endpoints"}

@router.get("/static/cases.css")
async def css():
    return FileResponse(os.path.join(STATIC, "cases.css"))

@router.get("/list")
async def api_list(goal: str = None, budget: str = None, persona: str = None):
    return list_cases(goal, budget, persona)

@router.get("/get/{case_id}")
async def api_get(case_id: str):
    c = get_case(case_id)
    if not c:
        return JSONResponse({"error":"not found"}, status_code=404)
    return c

@router.get("/catalog", response_class=HTMLResponse)
async def catalog(goal: str = None, budget: str = None, persona: str = None):
    items = list_cases(goal, budget, persona)
    t = env.get_template("catalog.html")
    return HTMLResponse(t.render(cases=items))

@router.get("/view/{case_id}", response_class=HTMLResponse)
async def view(case_id: str):
    c = get_case(case_id)
    if not c:
        return HTMLResponse("<h3>Кейс не найден</h3>", status_code=404)
    t = env.get_template("view.html")
    return HTMLResponse(t.render(case=c))

@router.get("/top_seller/{case_id}")
async def top_seller(case_id: str):
    c = get_case(case_id)
    if not c:
        return JSONResponse({"error":"not found"}, status_code=404)
    return {"answer": top_seller_reply(c)}

@router.get("/coach_pitch/{case_id}")
async def coach_pitch(case_id: str, tone: str = "firm"):
    c = get_case(case_id)
    if not c:
        return JSONResponse({"error":"not found"}, status_code=404)
    return {"pitch": coach_generate_pitch(c, tone)}

@router.get("/arena/{case_id}")
async def case_to_arena(case_id: str):
    c = get_case(case_id)
    if not c:
        return JSONResponse({"error":"not found"}, status_code=404)
    # отдаём контекст, который можно напрямую скормить spawn в arena_psychotypes
    return {"open": "/arena_psy/v1/spawn", "payload": {"difficulty":"hard","context": arena_context(c)}}

# Non-versioned endpoints
@router_noversion.post("/start")
async def start_telegram_noversion(req: Request):
    return await start_telegram(req)

@router_noversion.post("/start_session")
async def start_session_endpoint_noversion(req: Request):
    return await start_session_endpoint(req)

@router_noversion.post("/run")
async def run_endpoint_noversion(req: Request):
    return await run_endpoint(req)

@router_noversion.post("/init")
async def init_endpoint_noversion(req: Request):
    return await init_endpoint(req)

@router_noversion.get("/static/cases.css")
async def css_noversion():
    return await css()

@router_noversion.get("/list")
async def api_list_noversion(goal: str = None, budget: str = None, persona: str = None):
    return await api_list(goal, budget, persona)

@router_noversion.get("/get/{case_id}")
async def api_get_noversion(case_id: str):
    return await api_get(case_id)

@router_noversion.get("/catalog", response_class=HTMLResponse)
async def catalog_noversion(goal: str = None, budget: str = None, persona: str = None):
    return await catalog(goal, budget, persona)

@router_noversion.get("/view/{case_id}", response_class=HTMLResponse)
async def view_noversion(case_id: str):
    return await view(case_id)

@router_noversion.get("/top_seller/{case_id}")
async def top_seller_noversion(case_id: str):
    return await top_seller(case_id)

@router_noversion.get("/coach_pitch/{case_id}")
async def coach_pitch_noversion(case_id: str, tone: str = "firm"):
    return await coach_pitch(case_id, tone)

@router_noversion.get("/arena/{case_id}")
async def case_to_arena_noversion(case_id: str):
    return await case_to_arena(case_id)
