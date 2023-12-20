from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.routes.user_router import router as user_router
from app.routes.topic_router import router as topic_router
from app.models.models import Base
from app.database import engine, SessionLocal

Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(topic_router, prefix="/topics", tags=["topics"])

auth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def read_topics():
    return "Bem vindo a API do servdialogo"


# @app.post("/token", response_model=Token)
# def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = verify_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=60)
#     access_token = create_access_token(
#         data={"sub": user.nickname}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# def fake_verify_user(username: str, password: str):
#     return None