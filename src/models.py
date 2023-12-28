
from database import Base
from sqlalchemy import Column, String, Integer, DateTime, func


class User(Base):
    """
    用户（对象：老师 & 学生）

    Attributes:
        id (int): 用户索引，主键
        open_id (str): token，唯一标识符
        name (str, optional): 用户姓名
        admin_class (str, optional): 行政班级
        username (str): 账号
        number (str): 学号
        password (str): 密码
    """

    __tablename__ = "user"
    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    open_id = Column(String(40), nullable=False)
    name = Column(String(15), nullable=True)
    admin_class = Column(String(15), nullable=True)


class MyClass(Base):
    """
    创建班级（对象：老师）

    Attributes:
        class_id (int): 班级索引，主键
        id (int): 用户索引
        class_name (str, optional): 教学班级
        numbers (int, optional): 班级成员数量
        joinCode (str): 加入班级码
    """

    __tablename__ = "MyClass"
    class_id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    id = Column(Integer, nullable=False)
    class_name = Column(String(20), nullable=True)
    numbers = Column(Integer, nullable=True)
    joinCode = Column(String(20), nullable=False)


class JoinClass(Base):
    """
    加入班级（对象：学生）

    Attributes:
        class_id (int): 班级索引，主键
        id (int): 用户索引，主键
    """

    __tablename__ = "JoinClass"
    class_id = Column(Integer, primary_key=True, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)


class signInRecord(Base):
    """
    签到记录（对象：学生）

    Attributes:
        check_in_id (int): 签到索引，主键
        id (int): 用户索引，主键
        signIn_time (datetime): 签到时间
        signIn_status (int): 签到状态
    """

    __tablename__ = "signInRecord"
    check_in_id = Column(Integer, primary_key=True, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    signIn_time = Column(DateTime, nullable=False)
    signIn_status = Column(Integer, nullable=False)


class checkInRecord(Base):
    """
   发起签到（对象：老师）

   Attributes:
       check_in_id (int): 签到索引，主键
       id (int): 用户索引
       class_id (int): 班级索引
       start_time (datetime): 发起签到时间
       end_time (datetime): 结束签到时间
   """

    __tablename__ = "checkInRecord"
    check_in_id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    id = Column(Integer, nullable=False)
    class_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False, default=func.now())
    end_time = Column(DateTime, nullable=False, default=func.now())
