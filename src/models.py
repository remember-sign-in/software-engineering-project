
from database import Base
from sqlalchemy import Column, String, Integer, DateTime, func


class User(Base):
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    open_id = Column(String(40), index=True, nullable=False)
    name = Column(String(15), index=True, nullable=False)
    admin_class = Column(String(15), index=True, nullable=False)


class MyClass(Base):
    __tablename__ = "MyClass"
    class_id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(String(20), index=True, nullable=False)
    class_name = Column(String(20), index=True, nullable=False)
    numbers = Column(Integer, index=True, nullable=False)
    joinCode = Column(String(20), index=True, nullable=False)


class JoinClass(Base):
    __tablename__ = "JoinClass"
    class_id = Column(String(20), primary_key=True, index=True, nullable=False)
    student_id = Column(String(20), primary_key=True, index=True, nullable=False)


class signInRecord(Base):
    __tablename__ = "signInRecord"
    check_in_id = Column(String(15), primary_key=True, index=True, nullable=False)
    student_id = Column(String(15), index=True, nullable=False)
    signIn_time = Column(DateTime, index=True, nullable=False)
    signIn_status = Column(Integer, index=True, nullable=False)


class checkInRecord(Base):
    __tablename__ = "checkInRecord"
    check_in_id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(String(15), index=True, nullable=False)
    class_id = Column(String(15), index=True, nullable=False)
    start_time = Column(DateTime, index=True, nullable=False, default=func.now())
    end_time = Column(DateTime, index=True, nullable=False, default=func.now())
