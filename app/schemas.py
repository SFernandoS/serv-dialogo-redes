from pydantic import BaseModel, constr
from typing import List, Optional
from enum import Enum


class DialogCapability(str, Enum):
    CHAT = "chat"
    VIDEO_CALL = "video_call"
    BOTH = "both"


class UserStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"


class TopicBase(BaseModel):
    name: str


class TopicCreate(TopicBase):
    pass


class Topic(TopicBase):
    id: int
    interested_users: List[int] = []

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    nickname: constr(min_length=3, max_length=50)
    dialog_capability: DialogCapability
    status: Optional[UserStatus] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    interested_topics: List[Topic] = []

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    nickname: Optional[constr(min_length=3, max_length=50)] = None
    password: Optional[str] = None
    dialog_capability: Optional[DialogCapability] = None
    status: Optional[UserStatus] = None
