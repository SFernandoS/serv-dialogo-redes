from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum


Base = declarative_base()


class DialogCapability(PyEnum):
    CHAT = "chat"
    VIDEO_CALL = "video_call"
    BOTH = "both"


class UserStatus(PyEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"


user_topic_table = Table('user_topic', Base.metadata,
                         Column('user_id', Integer, ForeignKey('user.id')),
                         Column('topic_id', Integer, ForeignKey('topic.id'))
                         )


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    dialog_capability = Column(Enum(DialogCapability), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.OFFLINE)

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
