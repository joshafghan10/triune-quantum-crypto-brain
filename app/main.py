from __future__ import annotations

import asyncio
from pathlib import Path

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .simulator import DemoSimulator

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


def build_app() -> FastAPI:
    app = FastAPI(title="Triune Quantum Crypto Brain")
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

    async def start_simulator() -> DemoSimulator:
        sim = DemoSimulator()
        app.state.simulator = sim
        app.state.sim_task = asyncio.create_task(sim.run())
        return sim

    @app.on_event("startup")
    async def startup_event() -> None:
        await start_simulator()

    @app.get("/")
    async def index() -> HTMLResponse:
        return templates.TemplateResponse("index.html", {"title": "Triune Quantum Crypto Brain"})

    @app.get("/state")
    async def state() -> dict:
        return app.state.simulator.snapshot()

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket) -> None:
        await websocket.accept()
        queue = await app.state.simulator.bus.subscribe()
        await websocket.send_json({"event": "snapshot", "data": app.state.simulator.snapshot()})
        while True:
            msg = await queue.get()
            await websocket.send_json({"event": "message", "data": msg.model_dump(mode="json")})

    return app

app = build_app()
