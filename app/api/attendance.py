from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.attendance import Attendance, AttendanceType
from app.models.child import Child


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/attendance", name="attendance_page")
async def attendance_page(
    request: Request,
    db: Session = Depends(get_db),
    child_id: int | None = None,
):
    children = db.query(Child).order_by(Child.name).all()
    today = date.today()
    todays_records = (
        db.query(Attendance)
        .filter(Attendance.date == today)
        .order_by(Attendance.id.desc())
        .all()
    )
    return templates.TemplateResponse(
        "attendance.html",
        {
            "request": request,
            "children": children,
            "today": today,
            "records": todays_records,
            "selected_child_id": child_id,
        },
    )


@router.get("/scanner", name="qr_scanner")
async def qr_scanner(
    request: Request,
    mode: str | None = None,
):
    return templates.TemplateResponse(
        "scanner.html",
        {
            "request": request,
            "mode": mode or "attendance",
        },
    )


@router.post("/attendance/checkin")
async def attendance_checkin(
    request: Request,
    db: Session = Depends(get_db),
    child_id: int = Form(...),
    attendance_type: str = Form(...),
):
    today = date.today()

    existing = (
        db.query(Attendance)
        .filter(
            Attendance.child_id == child_id,
            Attendance.date == today,
            Attendance.type == AttendanceType(attendance_type),
        )
        .first()
    )
    if not existing:
        record = Attendance(
            child_id=child_id,
            servant_id=0,  # placeholder until servant users are wired
            type=AttendanceType(attendance_type),
            date=today,
        )
        db.add(record)
        db.commit()

    return RedirectResponse(url="/attendance", status_code=303)

