# app/services/user_service.py
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.db.models.user import User
from app.core import security
from app.schemas.user import UserCreate, UserUpdate


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_data: UserCreate) -> User:
    existing = get_user_by_email(db, user_data.email)
    if existing:
        raise ValueError("Email already registered")
    hashed_pw = security.hash_password(user_data.password)
    code = str(uuid.uuid4())[:8]
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pw,
        is_active=True,
        is_verified=False,
        is_admin=False,
        verification_code=code,
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"[Verification] User {new_user.email} code: {new_user.verification_code}")
    return new_user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Вернет пользователя, если пароль подходит, иначе None"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user

def update_user(db: Session, user: User, updates: UserUpdate) -> User:
    if updates.password:
        user.hashed_password = security.hash_password(updates.password)
    if updates.is_active is not None:
        user.is_active = updates.is_active
    if updates.is_admin is not None:
        user.is_admin = updates.is_admin
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
