from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.models.models import User
from app.schemas.schemas import UserCreate, UserUpdate
from werkzeug.security import generate_password_hash


def create_user(db: Session, user: UserCreate):
    hashed_password = generate_password_hash(user.password)
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
