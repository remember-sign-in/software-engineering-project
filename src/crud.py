import datetime
from typing import List

from sqlalchemy import DateTime

import schemas
from sqlalchemy.orm import Session
import models


# 获取用户的openid
def get_user_by_openid(db: Session, openid: str) -> models.User:
    return db.query(models.User).filter(models.User.open_id == openid).first()


# 创建用户
def create_user(db: Session, openid: str) -> models.User:
    db_user = models.User(open_id=openid)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 查询用户创建的班级
def get_my_class(db: Session, user_id: str) -> models.MyClass:
    return db.query(models.MyClass).filter(models.MyClass.user_id == user_id).all()


# 查询用户加入的班级
def get_join_class(db: Session, user_id: str) -> models.MyClass:
    db_joinclass_id = db.query(models.JoinClass).filter(models.JoinClass.user_id == user_id).all()
    if not db_joinclass_id: return None
    class_ids = [str(join_class.class_id) for join_class in db_joinclass_id]
    return db.query(models.MyClass).filter(models.MyClass.class_id.in_(class_ids)).all()


# 创建新班级
def create_class(db: Session, creator_id: str, name: str, joinCode: str, stuNum: int) -> models.MyClass:
    db_myclass = db.query(models.MyClass).filter(models.MyClass.joinCode == joinCode).first()
    if db_myclass:
        return None
    db_myclass = models.MyClass(user_id=creator_id, class_name=name, numbers=stuNum, joinCode=joinCode)
    db.add(db_myclass)
    db.commit()
    db.refresh(db_myclass)
    return db_myclass


# 获取目标id的班级学生列表
def get_class_list(db: Session, id: str) -> List[models.User] | None:
    db_joinclass = db.query(models.JoinClass).filter(models.JoinClass.class_id == id).all()
    if not db_joinclass:
        return None
    user_ids = [int(join_class.user_id) for join_class in db_joinclass]
    return db.query(models.User).filter(models.User.user_id.in_(user_ids)).all()


# 加入班级
def join_class(db: Session, id: str, joinCode: str) -> int:
    db_myclass = db.query(models.MyClass).filter(models.MyClass.joinCode == joinCode).first()
    if not db_myclass:
        return 0
    if not db.query(models.JoinClass).filter(
            models.JoinClass.user_id == id and models.JoinClass.class_id == db_myclass.class_id).first():
        db_joinclass = models.JoinClass(user_id=id, class_id=db_myclass.class_id)
        db.add(db_joinclass)
        db.commit()
        db.refresh(db_joinclass)
        return 1
    return -1


# 删除班级
def delete_class(db: Session, class_id: str) -> int:
    db_class = db.query(models.MyClass).filter(models.MyClass.class_id == class_id).first()
    if not db_class:
        return 0
    db.delete(db_class)
    db.commit()
    # 删除选该门课程的学生
    db_students = db.query(models.JoinClass).filter(models.JoinClass.class_id == class_id).all()
    for student in db_students:
        db.delete(student)
    db.commit()
    return 1


def StartSign(db: Session, startsign: schemas.sign) -> int:
    db_class = db.query(models.MyClass).filter(models.MyClass.class_id == startsign.class_id).first()
    if not db_class:
        return 0
    db_checkIn = models.checkInRecord(user_id=startsign.user_id, class_id=startsign.class_id,
                                      start_time=startsign.starttime, end_time=startsign.endtime)
    db.add(db_checkIn)
    db.commit()
    db.refresh(db_checkIn)
    return 1


#
def EndSign(db: Session, user_id: str, class_id: str, datetime: DateTime) -> int:
    db_class = db.query(models.checkInRecord).filter(
        models.checkInRecord.class_id == class_id and models.checkInRecord.user_id == user_id).first()
    if not db_class:
        return 0
    current_time = datetime.now()
    if current_time > db_class.end_time:
        return 2
    if current_time < db_class.end_time:
        db_class.end_time = current_time
    return 1
#
# def signUp(db: Session, user_id: str, class_id: str) -> int:
#     db_checkIn_id = db.query(models.checkInRecord).filter(models.checkInRecord.check_in_id).first()
#     return 0
