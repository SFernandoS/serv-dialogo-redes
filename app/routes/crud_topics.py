from sqlalchemy.orm import Session
from models.models import Topic
from schemas.schemas import TopicCreate


def create_topic(db: Session, topic_data: TopicCreate):
    db_topic = Topic(name=topic_data.name)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def get_topics(db: Session):
    return db.query(Topic).all()


def get_topic(db: Session, topic_id: int):
    return db.query(Topic).filter(Topic.id == topic_id).first()


def update_topic(db: Session, topic_id: int, topic_data: TopicCreate):
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if db_topic is None:
        return None
    db_topic.name = topic_data.name
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def delete_topic(db: Session, topic_id: int):
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if db_topic:
        db.delete(db_topic)
        db.commit()
        return db_topic
