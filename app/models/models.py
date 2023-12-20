from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base


user_topic_table = Table('user_topic', Base.metadata,
                         Column('user_id', Integer, ForeignKey('user.id')),
                         Column('topic_id', Integer, ForeignKey('topic.id'))
                         )


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    dialog_capability = Column(String, nullable=False)
    status = Column(String, nullable=False)

    interested_topics = relationship(
        "Topic",
        secondary=user_topic_table,
        back_populates="interested_users"
    )


class Topic(Base):
    __tablename__ = 'topic'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    interested_users = relationship(
        "User",
        secondary=user_topic_table,
        back_populates="interested_topics"
    )
