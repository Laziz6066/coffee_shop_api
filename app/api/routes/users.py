from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import dependencies as deps
from app.schemas.user import UserOut, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def read_current_user(current_user = Depends(deps.get_current_user)):
    """
    Возвращает данные текущего авторизованного пользователя.
    """
    return current_user  # Pydantic схема UserOut преобразует объект


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(deps.get_db), admin_user = Depends(deps.get_current_admin)):
    """
    Для администратора: получить список всех пользователей.
    """
    users = db.query(user_service.User).all()  # можно импортировать модель User напрямую
    return users


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(deps.get_db), admin_user = Depends(deps.get_current_admin)):
    """
    Для администратора: получить данные конкретного пользователя по ID.
    """
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, updates: UserUpdate, db: Session = Depends(deps.get_db), admin_user = Depends(deps.get_current_admin)):
    """
    Для администратора: частично обновить пользователя (активность, роль или пароль).
    """
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated = user_service.update_user(db, user, updates)
    return updated


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(deps.get_db), admin_user = Depends(deps.get_current_admin)):
    """
    Для администратора: удалить пользователя.
    """
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_service.delete_user(db, user)
    return {"detail": "User deleted"}
