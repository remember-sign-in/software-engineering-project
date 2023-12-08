from database import Base
from sqlalchemy import Column, String, Integer


class User(Base):
    __tablename__ = "user"
    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    open_id = Column(String(40), index=True, nullable=False)
