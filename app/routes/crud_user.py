from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from models.models import User
from schemas.schemas import UserCreate, UserUpdate
from werkzeug.security import generate_password_hash


def create_user(db: Session, user: UserCreate):
    hashed_password = generate_password_hash(user.password)
    db_user = User(
        nickname=user.nickname,
        password_hash=hashed_password,
        dialog_capability=user.dialog_capability,
        status=user.status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).options(joinedload(User.interested_topics)).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return None
    for var, value in vars(user).items():
        if value:
            setattr(db_user, var, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
