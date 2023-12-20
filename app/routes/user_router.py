from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.routes.crud_user import create_user, get_users, get_user
from app.schemas.schemas import User, UserCreate, UserUpdate
from app.models.models import Base
from app.database import engine, SessionLocal
from fastapi.security import OAuth2PasswordBearer


Base.metadata.create_all(bind=engine)


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/users/", response_model=List[User])
def read_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    users = get_users(db)
    return users


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
