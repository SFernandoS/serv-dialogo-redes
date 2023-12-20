from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from routes.crud_topics import create_topic, get_topic, get_topics
from schemas.schemas import Topic, TopicCreate
from database import engine, SessionLocal
from models.models import Base


Base.metadata.create_all(bind=engine)


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/topics/", response_model=Topic, status_code=status.HTTP_201_CREATED)
def create_topic_route(topic: TopicCreate, db: Session = Depends(get_db)):
    return create_topic(db, topic)


@router.get("/topics/", response_model=List[Topic])
def read_topics(db: Session = Depends(get_db)):
    topics = get_topics(db)
    return topics


@router.get("/topics/{topic_id}", response_model=Topic)
def read_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.put("/topics/{topic_id}", response_model=Topic)
def update_topic(topic_id: int, topic: TopicCreate, db: Session = Depends(get_db)):
    updated_topic = update_topic(db, topic_id, topic)
    if updated_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return updated_topic


@router.delete("/topics/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = delete_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"message": "Topic deleted"}
