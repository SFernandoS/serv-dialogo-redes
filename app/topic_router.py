from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import crud_topics, schemas
from app.database import AsyncSessionLocal


router = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/topics/", response_model=schemas.Topic, status_code=status.HTTP_201_CREATED)
async def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    return await crud_topics.create_topic(db, topic)


@router.get("/topics/", response_model=List[schemas.Topic])
async def read_topics(db: Session = Depends(get_db)):
    topics = await crud_topics.get_topics(db)
    return topics


@router.get("/topics/{topic_id}", response_model=schemas.Topic)
async def read_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = await crud_topics.get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.put("/topics/{topic_id}", response_model=schemas.Topic)
async def update_topic(topic_id: int, topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    updated_topic = await crud_topics.update_topic(db, topic_id, topic)
    if updated_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return updated_topic


@router.delete("/topics/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = await crud_topics.delete_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"message": "Topic deleted"}
