from collections import defaultdict
from datetime import date
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.child import Child
from app.models.points import Points
from app.models.attendance import Attendance
from app.models.visit import Visit


def list_children_with_points(db: Session) -> List[dict]:
    children = db.query(Child).order_by(Child.name).all()

    # Aggregate points per child
    points_rows = (
        db.query(Points.child_id, func.coalesce(func.sum(Points.points), 0))
        .group_by(Points.child_id)
        .all()
    )
    points_map: dict[int, int] = {child_id: total for child_id, total in points_rows}

    result: List[dict] = []
    for child in children:
        result.append(
            {
                "child": child,
                "points": points_map.get(child.id, 0),
            }
        )
    return result


def get_child_with_history(db: Session, child_id: int) -> Optional[dict]:
    child = db.query(Child).filter(Child.id == child_id).first()
    if not child:
        return None

    attendances = (
        db.query(Attendance)
        .filter(Attendance.child_id == child_id)
        .order_by(Attendance.date.desc())
        .all()
    )
    visits = (
        db.query(Visit)
        .filter(Visit.child_id == child_id)
        .order_by(Visit.date.desc())
        .all()
    )
    points = (
        db.query(Points)
        .filter(Points.child_id == child_id)
        .order_by(Points.date.desc())
        .all()
    )

    total_points = sum(p.points for p in points)

    return {
        "child": child,
        "attendances": attendances,
        "visits": visits,
        "points": points,
        "total_points": total_points,
    }


def create_child(
    db: Session,
    *,
    name: str,
    age: int | None,
    stage: str,
    grade: str | None,
    phone: str | None,
    father_phone: str | None,
    mother_phone: str | None,
    confession_number: str | None,
    address: str | None,
    school: str | None,
    notes: str | None,
):
    child = Child(
        name=name,
        age=age,
        stage=stage,
        grade=grade,
        phone=phone,
        father_phone=father_phone,
        mother_phone=mother_phone,
        confession_number=confession_number,
        address=address,
        school=school,
        notes=notes,
    )
    db.add(child)
    db.commit()
    db.refresh(child)
    return child

