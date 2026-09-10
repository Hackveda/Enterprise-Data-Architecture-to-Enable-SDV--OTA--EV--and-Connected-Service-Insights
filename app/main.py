from __future__ import annotations

import asyncio
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import get_settings
from app.services.live import TEAMS, live_snapshot
from app.services.snowflake import health as snowflake_health, team_kpis
from app.services.study import team_payload

BASE = Path(__file__).resolve().parent
app = FastAPI(title="Automotive Enterprise Data Platform", version="2.0.0")
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")
templates = Jinja2Templates(directory=BASE / "templates")

@app.get("/health")
def health():
    return {"status": "ok", "snowflake": snowflake_health()}

@app.get("/api/snowflake/health")
def sf_health():
    return snowflake_health()

@app.get("/api/team/{team}/data")
def team_data(team: str):
    if team not in TEAMS: raise HTTPException(404, "Unknown team")
    return {"team": team, "live": live_snapshot(team, 0), "governed": team_kpis(team), **team_payload(team)}

@app.get("/api/team/{team}/stream")
async def team_stream(team: str):
    if team not in TEAMS: raise HTTPException(404, "Unknown team")
    async def events():
        tick = 0
        while True:
            yield f"event: metric\ndata: {json.dumps(live_snapshot(team, tick))}\n\n"
            tick += 1
            await asyncio.sleep(1)
    return StreamingResponse(events(), media_type="text/event-stream", headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "team": "marketing", "settings": get_settings()})

@app.get("/{team}", response_class=HTMLResponse)
def team_page(request: Request, team: str):
    if team not in TEAMS: raise HTTPException(404, "Unknown team")
    return templates.TemplateResponse("index.html", {"request": request, "team": team, "settings": get_settings()})
