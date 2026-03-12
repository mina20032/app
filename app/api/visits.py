from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.child import Child
from app.models.visit import Visit


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/visits", name="visits_page")
async def visits_page(
    request: Request,
    db: Session = Depends(get_db),
    child_id: int | None = None,
):
    children = db.query(Child).order_by(Child.name).all()
    visits = db.query(Visit).order_by(Visit.date.desc()).limit(50).all()
    return templates.TemplateResponse(
        "visits.html",
        {
            "request": request,
            "children": children,
            "selected_child_id": child_id,
            "visits": visits,
        },
    )


@router.post("/visits")
async def visits_create(
    request: Request,
    db: Session = Depends(get_db),
    child_id: int = Form(...),
    visit_date: date = Form(...),
    notes: str = Form(""),
):
    visit = Visit(
        child_id=child_id,
        servant_id=0,  
        date=visit_date,
        notes=notes,
    )
    db.add(visit)
    db.commit()

    return RedirectResponse(url="/visits", status_code=303)

