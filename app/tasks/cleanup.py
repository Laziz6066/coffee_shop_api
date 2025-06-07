# app/tasks/cleanup.py
from celery import Celery
from datetime import datetime, timedelta
from app.core.config import settings
from app.db.database import SessionLocal
from app.db.models.user import User

# Инициализируем Celery
celery_app = Celery("coffee_shop_tasks", broker=settings.CELERY_BROKER_URL)
celery_app.conf.result_backend = settings.CELERY_RESULT_BACKEND

# Определяем периодическую задачу (каждые 24 часа)
# (Если используем celery beat, можно настроить расписание здесь или в отдельном конфиге)
celery_app.conf.beat_schedule = {
    "cleanup-unverified-everyday": {
        "task": "app.tasks.cleanup.delete_unverified_users",
        "schedule": 60.0 * 60.0 * 24.0  # раз в сутки
    }
}

@celery_app.task
def delete_unverified_users():
    """
    Удаляет из базы всех пользователей, которые не подтвердили email в течение 2 дней.
    """
    db = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(days=2)
        db.query(User).filter(User.is_verified == False, User.created_at < cutoff).delete()
        db.commit()
    finally:
        db.close()
