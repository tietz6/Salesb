
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os, json
from .service import list_catalog, get_lesson, score_test, recommend_lessons

router = APIRouter(prefix="/edu_lessons/v1", tags=["edu_lessons"])
router_noversion = APIRouter(prefix="/edu_lessons", tags=["edu_lessons"])

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
    
    return {"ok": True, "message": "Edu Lessons module - use /catalog, /list, /lesson endpoints"}

@router.post("/start_session")
async def start_session_endpoint(req: Request):
    """Session start endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Edu Lessons module - use /catalog, /list, /lesson endpoints"}

@router.post("/run")
async def run(req: Request):
    """Run endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Edu Lessons module - use /catalog, /list, /lesson endpoints"}

@router.post("/init")
async def init(req: Request):
    """Init endpoint"""
    data = await req.json()
    probe = data.get("probe", False)
    
    if probe:
        return {"ok": True, "available": True}
    
    return {"ok": True, "message": "Edu Lessons module - use /catalog, /list, /lesson endpoints"}

@router.get("/static/edu.css")
async def css():
    return FileResponse(os.path.join(STATIC,"edu.css"))

@router.get("/catalog", response_class=HTMLResponse)
async def catalog():
    items = list_catalog()
    t = env.get_template("catalog.html")
    return HTMLResponse(t.render(lessons=items))

@router.get("/view/{cat}/{name}", response_class=HTMLResponse)
async def view(cat: str, name: str):
    lid = f"{cat}/{name}"
    l = get_lesson(lid)
    if not l:
        return HTMLResponse("<h3>Урок не найден</h3>", status_code=404)
    t = env.get_template("view.html")
    return HTMLResponse(t.render(lesson=l))

@router.get("/test/{cat}/{name}", response_class=HTMLResponse)
async def test_view(cat: str, name: str):
    lid = f"{cat}/{name}"
    l = get_lesson(lid)
    if not l:
        return HTMLResponse("<h3>Урок не найден</h3>", status_code=404)
    t = env.get_template("test.html")
    return HTMLResponse(t.render(lesson=l))

@router.get("/list")
async def api_list():
    return list_catalog()

@router.get("/lesson/{cat}/{name}")
async def api_lesson(cat: str, name: str):
    lid = f"{cat}/{name}"
    l = get_lesson(lid)
    if not l:
        return JSONResponse({"error":"not found"}, status_code=404)
    return l

@router.post("/test/{cat}/{name}")
async def api_test(cat: str, name: str, req: Request):
    lid = f"{cat}/{name}"
    l = get_lesson(lid)
    if not l:
        return JSONResponse({"error":"not found"}, status_code=404)
    data = await req.json()
    ans = data.get("answer")
    return score_test(l, ans)

@router.get("/recommend/{manager_id}")
async def api_recommend(manager_id: str):
    return {"recommend": recommend_lessons(manager_id)}

# Non-versioned endpoints
@router_noversion.post("/start")
async def start_telegram_noversion(req: Request):
    return await start_telegram(req)

@router_noversion.post("/start_session")
async def start_session_endpoint_noversion(req: Request):
    return await start_session_endpoint(req)

@router_noversion.post("/run")
async def run_noversion(req: Request):
    return await run(req)

@router_noversion.post("/init")
async def init_noversion(req: Request):
    return await init(req)

@router_noversion.get("/static/edu.css")
async def css_noversion():
    return await css()

@router_noversion.get("/catalog", response_class=HTMLResponse)
async def catalog_noversion():
    return await catalog()

@router_noversion.get("/view/{cat}/{name}", response_class=HTMLResponse)
async def view_noversion(cat: str, name: str):
    return await view(cat, name)

@router_noversion.get("/test/{cat}/{name}", response_class=HTMLResponse)
async def test_view_noversion(cat: str, name: str):
    return await test_view(cat, name)

@router_noversion.get("/list")
async def api_list_noversion():
    return await api_list()

@router_noversion.get("/lesson/{cat}/{name}")
async def api_lesson_noversion(cat: str, name: str):
    return await api_lesson(cat, name)

@router_noversion.post("/test/{cat}/{name}")
async def api_test_noversion(cat: str, name: str, req: Request):
    return await api_test(cat, name, req)

@router_noversion.get("/recommend/{manager_id}")
async def api_recommend_noversion(manager_id: str):
    return await api_recommend(manager_id)
