from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import Settings, get_settings
from app.core.database import init_db
from app.api.routes import api_router


templates = Jinja2Templates(directory="templates")


def create_app() -> FastAPI:
    settings: Settings = get_settings()

    app = FastAPI(
        title="Church Sunday School System",
        description="QR-based attendance and management system for Sunday school",
        version="1.0.0",
    )

    # Initialize DB (for first run, idempotent)
    init_db()

    # Routers
    app.include_router(api_router)

    # Static files
    app.mount("/static", StaticFiles(directory="static"), name="static")

    return app


app = create_app()


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def root_redirect():
    """
    Redirect root to the main dashboard UI.
    """
    return RedirectResponse(url="/dashboard")


@app.get("/home", tags=["ui"], response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

