# database.py文件创建与数据库的连接
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from data.data import SQLALCHEMY_DATABASE_URL


# 启动引擎，删除encoding参数
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

# 启动会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 返回一个类，后续作为数据库模型的基类(ORM模型)
Base = declarative_base()
