from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import dependencies as deps
from app.schemas.user import UserOut, UserCreate, Token, UserLogin
from app.services import user_service
from app.core import security


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(deps.get_db)):
    """
    Регистрирует нового пользователя. Выводит код подтверждения в лог.
    """
    try:
        new_user = user_service.create_user(db, user_data)
    except ValueError as e:
        # Например, email уже существует
        raise HTTPException(status_code=400, detail=str(e))
    return new_user


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(deps.get_db)):
    """
    Аутентификация пользователя, возвращает JWT токен.
    """
    user = user_service.authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not verified")
    # Генерируем JWT
    token = security.create_access_token(user_id=user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/verify")
def verify_email(email: str, code: str, db: Session = Depends(deps.get_db)):
    """
    Подтверждение email пользователя по коду.
    """
    user = user_service.get_user_by_email(db, email=email)
    if not user or user.is_verified:
        raise HTTPException(status_code=400, detail="Invalid or already verified user")
    if user.verification_code != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    user.is_verified = True
    user.verification_code = None
    db.commit()
    return {"detail": "Email verified. You can now login."}
