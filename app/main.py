from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from werkzeug.security import check_password_hash
from sqlalchemy.orm import Session
from app.routes.user_router import router as user_router
from app.routes.topic_router import router as topic_router
from app.models.models import Base
from app.database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from app.models.models import User
from app.auth import create_access_token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user_from_token
from typing import Dict
import json

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(topic_router, prefix="/topics", tags=["topics"])


@app.get("/")
def read_topics():
    return "Bem vindo a API do servdialogo"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = db.query(User).filter(User.email == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = authenticate_user(db, form_data.username, form_data.password)
    db.close()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    current_user = get_current_user_from_token(token, db)
    db.close()
    return current_user


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_private_message(self, message: str, receiver_id: str):
        receiver = self.active_connections.get(receiver_id)
        if receiver:
            await receiver.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            json_data = await websocket.receive_text()
            data = json.loads(json_data)
            receiver_id = data["receiver_id"]
            message = data["message"]
            await manager.send_private_message(f"Message from {user_id}: {message}", receiver_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
