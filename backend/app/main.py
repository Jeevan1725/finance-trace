from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.core.config import get_settings
from app.routers import (
    cases, entities, relationships, documents,
    transactions, accounts, graph, reports, alerts, auth
)

settings = get_settings()
app = FastAPI(title=settings.APP_NAME, version="0.1.0")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cases.router)
app.include_router(entities.router)
app.include_router(relationships.router)
app.include_router(documents.router)
app.include_router(transactions.router)
app.include_router(accounts.router)
app.include_router(graph.router)
app.include_router(reports.router)
app.include_router(alerts.router)

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENV}

@app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
def dashboard():
    p = Path("/app/app/static/dashboard.html")
    return p.read_text(encoding="utf-8") if p.exists() else "<h1>Not found</h1>"

@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_page():
    p = Path("/app/app/static/login.html")
    return p.read_text(encoding="utf-8") if p.exists() else "<h1>Not found</h1>"

@app.get("/graph-ui", response_class=HTMLResponse, include_in_schema=False)
def graph_ui():
    p = Path("/app/app/static/graph.html")
    return p.read_text(encoding="utf-8") if p.exists() else "<h1>Not found</h1>"