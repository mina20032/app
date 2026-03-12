from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.child import Child
from app.models.attendance import Attendance
from app.models.visit import Visit
from app.models.points import Points


def get_dashboard_stats(db: Session) -> dict:
    today = date.today()

    total_children = db.query(func.count(Child.id)).scalar() or 0
    todays_attendance = (
        db.query(func.count(Attendance.id))
        .filter(Attendance.date == today)
        .scalar()
        or 0
    )
    total_visits = db.query(func.count(Visit.id)).scalar() or 0
    total_points = db.query(func.coalesce(func.sum(Points.points), 0)).scalar() or 0

    return {
        "total_children": total_children,
        "todays_attendance": todays_attendance,
        "total_visits": total_visits,
        "total_points": total_points,
    }

