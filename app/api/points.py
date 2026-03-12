from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.child import Child
from app.models.points import Points


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/points", name="points_page")
async def points_page(
    request: Request,
    db: Session = Depends(get_db),
    child_id: int | None = None,
):
    children = db.query(Child).order_by(Child.name).all()
    recent_points = db.query(Points).order_by(Points.date.desc()).limit(50).all()
    return templates.TemplateResponse(
        "points.html",
        {
            "request": request,
            "children": children,
            "selected_child_id": child_id,
            "points": recent_points,
        },
    )


@router.post("/points")
async def points_add(
    request: Request,
    db: Session = Depends(get_db),
    child_id: int = Form(...),
    amount: int = Form(...),
    reason: str = Form(""),
    points_date: date = Form(...),
):
    entry = Points(
        child_id=child_id,
        servant_id=0,  # placeholder
        points=amount,
        reason=reason,
        date=points_date,
    )
    db.add(entry)
    db.commit()

    return RedirectResponse(url="/points", status_code=303)

