# Importa bibliotecas necessárias
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from app.websocket import ConnectionManager
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
import json

# Criação de tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI()

# Adiciona middleware para lidar com CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função para obter uma instância de conexão com o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inclui as rotas definidas nos arquivos user_router e topic_router
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(topic_router, prefix="/topics", tags=["topics"])

# Rota de boas-vindas
@app.get("/")
def read_topics():
    return "Bem vindo a API do servdialogo"

# Define o esquema de autenticação OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Função para obter o usuário atual a partir do token
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = db.query(User).filter(User.email == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais de autenticação inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Rota para obter o token de acesso
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = authenticate_user(db, form_data.username, form_data.password)
    db.close()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Instância do ConnectionManager para gerenciar conexões WebSocket
manager = ConnectionManager()

# Rota WebSocket para comunicação de usuário para usuário
@app.websocket("/ws/user/{user_id}")
async def websocket_user_chat(websocket: WebSocket, user_id: str, token: str = Depends(oauth2_scheme)):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            await manager.send_private_message(message_data["message"], message_data["receiver"])
    except WebSocketDisconnect:
        manager.disconnect(user_id)

# Rota WebSocket para comunicação em tópico específico
@app.websocket("/ws/topic/{user_id}/{topic_id}")
async def websocket_topic_chat(websocket: WebSocket, user_id: str, topic_id: int, token: str = Depends(oauth2_scheme)):
    await manager.connect(websocket, user_id)
    await manager.join_topic(user_id, topic_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_topic_message(f"{user_id} diz: {data}", topic_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
