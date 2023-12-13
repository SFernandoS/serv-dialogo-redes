from sqlalchemy.orm import Session
from . import models, schemas


async def create_topic(db: Session, topic_data: schemas.TopicCreate):
    db_topic = models.Topic(name=topic_data.name)
    db.add(db_topic)
    await db.commit()
    await db.refresh(db_topic)
    return db_topic


async def get_topics(db: Session):
    return db.query(models.Topic).all()


async def get_topic(db: Session, topic_id: int):
    return db.query(models.Topic).filter(models.Topic.id == topic_id).first()


async def update_topic(db: Session, topic_id: int, topic_data: schemas.TopicCreate):
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if db_topic is None:
        return None
    db_topic.name = topic_data.name
    db.add(db_topic)
    await db.commit()
    await db.refresh(db_topic)
    return db_topic


async def delete_topic(db: Session, topic_id: int):
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if db_topic:
        db.delete(db_topic)
        await db.commit()
        return db_topic
