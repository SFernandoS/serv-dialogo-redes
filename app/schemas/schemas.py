from pydantic import BaseModel, constr
from typing import List, Optional


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
    email: str
    dialog_capability: str
    status: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    interested_topics: List[Topic] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    nickname: Optional[constr(min_length=3, max_length=50)] = None
    password: Optional[str] = None
    dialog_capability: Optional[str] = None
    status: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
