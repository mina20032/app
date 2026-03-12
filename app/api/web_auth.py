from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth.security import create_access_token, verify_password
from app.core.database import get_db
from app.models.user import User, UserRole


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login", name="login_page")
async def login_page(request: Request):
  return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_submit(
    request: Request,
    db: Session = Depends(get_db),
    password: str = Form(...),
):
    # Single-admin login: find first ADMIN user and check password only
    user = db.query(User).filter(User.role == UserRole.ADMIN).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid credentials",
            },
            status_code=400,
        )

    token = create_access_token(subject=user.id, role=user.role.value)
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        secure=False,
        samesite="lax",
    )
    return response

