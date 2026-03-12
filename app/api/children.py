from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.child import Stage
from app.models.user import User
from app.services.child_service import list_children_with_points, get_child_with_history, create_child
from app.utils.qr import generate_child_qr_base64, generate_child_qr_bytes


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/children", name="children_list")
async def children_list(
    request: Request,
    db: Session = Depends(get_db),
):
    children_with_points = list_children_with_points(db)
    return templates.TemplateResponse(
        "children.html",
        {
            "request": request,
            "user": None,
            "children": children_with_points,
        },
    )


@router.get("/children/new", name="children_new")
async def children_new_get(
    request: Request,
):
    return templates.TemplateResponse(
        "add_child.html",
        {
            "request": request,
            "user": None,
            "stages": [Stage.PRIMARY.value, Stage.PREP.value, Stage.SECONDARY.value],
        },
    )


@router.post("/children/new")
async def children_new_post(
    request: Request,
    db: Session = Depends(get_db),
    name: str = Form(...),
    age: int | None = Form(None),
    stage: str = Form(...),
    grade: str | None = Form(None),
    phone: str | None = Form(None),
    father_phone: str | None = Form(None),
    mother_phone: str | None = Form(None),
    confession_number: str | None = Form(None),
    address: str | None = Form(None),
    school: str | None = Form(None),
    notes: str | None = Form(None),
):
    create_child(
        db,
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
    return RedirectResponse(url="/children", status_code=303)


@router.get("/children/{child_id}", name="child_profile")
async def child_profile(
    child_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    data = get_child_with_history(db, child_id)
    if not data:
        raise HTTPException(status_code=404, detail="Child not found")

    qr_code_base64 = generate_child_qr_base64(child_id)

    return templates.TemplateResponse(
        "child_profile.html",
        {
            "request": request,
            "user": None,
            "child": data["child"],
            "attendances": data["attendances"],
            "visits": data["visits"],
            "points": data["points"],
            "total_points": data["total_points"],
            "qr_code_base64": qr_code_base64,
        },
    )


@router.get("/children/{child_id}/card", name="child_card")
async def child_card(
    child_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    data = get_child_with_history(db, child_id)
    if not data:
        raise HTTPException(status_code=404, detail="Child not found")

    qr_code_base64 = generate_child_qr_base64(child_id)

    return templates.TemplateResponse(
        "child_card.html",
        {
            "request": request,
            "child": data["child"],
            "qr_code_base64": qr_code_base64,
        },
    )


@router.get("/children/{child_id}/qr-download", name="child_qr_download")
async def child_qr_download(
    child_id: int,
    db: Session = Depends(get_db),
):
    data = get_child_with_history(db, child_id)
    if not data:
        raise HTTPException(status_code=404, detail="Child not found")

    png_bytes = generate_child_qr_bytes(child_id)
    filename = f"{data['child'].name.replace(' ', '_')}_qr.png"

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }

    return Response(
        content=png_bytes,
        media_type="image/png",
        headers=headers,
    )

