import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import health, dashboard, players, wars, raids, tracked_clans

app = FastAPI(title="Clash Tracker API", version="0.1.0")

_extra_origins = os.environ.get("CORS_ORIGINS", "").split(",")
_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    *[o.strip() for o in _extra_origins if o.strip()],
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(dashboard.router)
app.include_router(players.router)
app.include_router(wars.router)
app.include_router(raids.router)
app.include_router(tracked_clans.router)
