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
    id: int
    name: str
    joinCode: str
    stuNum: int


class ClassJoin(BaseModel):
    id: int
    joinCode: str


class sign(BaseModel):
    id: int
    class_id: int
    starttime: datetime
    endtime: datetime

    class Config:
        from_attributes = True
