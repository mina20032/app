from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dependencies import login_for_access_token, get_current_user
from app.models.user import User
from app.schemas.user import Token, UserRead


router = APIRouter()


@router.post("/login", response_model=Token, summary="Obtain access token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Login with email (as `username`) and password using form data.
    Returns a JWT bearer token.
    """
    return await login_for_access_token(form_data)


@router.get("/me", response_model=UserRead)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user

