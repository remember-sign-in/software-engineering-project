from pydantic import BaseModel



class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    openid: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
