from fastapi import FastAPI
from app.user_router import router as user_router
from app.topic_router import router as topic_router
from app.database import init_db


app = FastAPI()


async def startup_event():
    await init_db()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(topic_router, prefix="/topics", tags=["topics"])


@app.get("/")
async def read_topics():
    return "Bem vindo a API do servdialogo"
