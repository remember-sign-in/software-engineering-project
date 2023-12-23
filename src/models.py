from database import Base
from sqlalchemy import Column, String, Integer


class User(Base):
    __tablename__ = "user"
    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    open_id = Column(String(40), nullable=False)
    name = Column(String(15), nullable=True)
    admin_class = Column(String(15), nullable=True)


class MyClass(Base):
    __tablename__ = "MyClass"
    class_id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(String(15), index=True, nullable=False)
    class_name = Column(String(15), index=True, nullable=False)
    numbers = Column(Integer, index=True, nullable=False)
    joinCode = Column(String(15), index=True, nullable=False)


class JoinClass(Base):
    __tablename__ = "JoinClass"
    class_id = Column(String(15), primary_key=True, index=True, nullable=False)
    user_id = Column(String(15), primary_key=True, index=True, nullable=False)
