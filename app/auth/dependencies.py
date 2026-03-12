from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.security import verify_password
from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import Token, TokenPayload, UserRoleEnum
from app.auth.security import create_access_token, decode_access_token
from app.services.user_service import get_user_by_email


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(subject=user.id, role=user.role.value)
    return Token(access_token=token)


def get_current_user(
    request: Request,
    token: Annotated[Optional[str], Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Prefer Authorization header, then cookie
    raw_token = token
    if not raw_token:
        raw_token = request.cookies.get("access_token")
    if not raw_token:
        raise credentials_exception

    # Cookie may store "Bearer xxx"
    if raw_token.startswith("Bearer "):
        raw_token = raw_token.split(" ", 1)[1]

    try:
        payload = decode_access_token(raw_token)
        token_data = TokenPayload(sub=int(payload.get("sub")), role=UserRoleEnum(payload.get("role")))
    except Exception:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.sub).first()
    if user is None:
        raise credentials_exception
    return user


def require_admin(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user


def require_servant_or_admin(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role not in (UserRole.ADMIN, UserRole.SERVANT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return current_user

