from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import DateTime
from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class ClassBase(BaseModel):
    pass


class UserCreate(UserBase):
    openid: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class ClassCreate(ClassBase):
    creator_id: str
    name: str
    joinCode: str
    stuNum: int


class ClassJoin(BaseModel):
    id: str
    joinCode: str


class sign(BaseModel):
    user_id: str
    class_id: str
    starttime: datetime
    endtime: datetime

    class Config:
        from_attributes = True
