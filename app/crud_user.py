from sqlalchemy.orm import Session
from . import models, schemas
from werkzeug.security import generate_password_hash


async def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = generate_password_hash(user.password)
    db_user = models.User(
        nickname=user.nickname,
        password_hash=hashed_password,
        dialog_capability=user.dialog_capability,
        status=user.status
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_users(db: Session):
    return db.query(models.User).all()


async def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


async def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    for var, value in vars(user).items():
        if value:
            setattr(db_user, var, value)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        await db.commit()
        return db_user
