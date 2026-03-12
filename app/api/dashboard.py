from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard_service import get_dashboard_stats


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/dashboard", name="dashboard")
async def dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    stats = get_dashboard_stats(db)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": None,
            "stats": stats,
        },
    )

