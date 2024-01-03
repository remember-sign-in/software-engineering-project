from datetime import datetime, timedelta
import random, string
from random import choice
import responses
from typing import List, Dict, Any

from sqlalchemy import DateTime, desc, case

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


def login_user(username: str, password: str, db: Session):
    db_login = db.query(models.User).filter(models.User.username == username, models.User.password == password).first
    if db_login is None:
        return db_login
    else:
        return 0


# 查询用户创建的班级
def get_my_class(db: Session, id: int) -> models.MyClass:
    return db.query(models.MyClass).filter(models.MyClass.id == id).all()


def get_search_class(class_name, db: Session) -> models.MyClass:
    return db.query(models.MyClass).filter(models.MyClass.class_name == class_name).first()


# 查询用户加入的班级
def get_join_class(db: Session, id: int) -> [models.MyClass]:
    db_joinclass_id = db.query(models.JoinClass).filter(models.JoinClass.id == id).all()
    if not db_joinclass_id:
        return None
    class_ids = [str(join_class.class_id) for join_class in db_joinclass_id]
    result = db.query(models.MyClass).filter(models.MyClass.class_id.in_(class_ids)).all()
    return result


def exit_class(id: int, class_id: int, db: Session) -> int:
    db_exitclass = db.query(models.JoinClass).filter(models.JoinClass.id == id,
                                                     models.JoinClass.class_id == class_id).first()
    db_createclass = db.query(models.MyClass).filter(models.MyClass.class_id == class_id,
                                                     models.MyClass.id == id).first()
    if db_createclass:
        return 0
    if db_exitclass:
        db.delete(db_exitclass)
        db.commit()
        return 1
    else:
        return -1


def kick_class(id: int, class_id: int, db: Session) -> int:
    db_exitclass = db.query(models.JoinClass).filter(models.JoinClass.id == id,
                                                     models.JoinClass.class_id == class_id).first()
    db_createclass = db.query(models.MyClass).filter(models.MyClass.class_id ==class_id,models.MyClass.id == id).first()
    if db_createclass:
        return 0
    if db_exitclass:
        db.delete(db_exitclass)
        db.commit()
        return 1
    else:
        return -1


# 创建新班级
def create_class(id: int, name: str, stuNum: int, db: Session) -> models.MyClass:
    joinCode = result = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    db_myclass = db.query(models.MyClass).filter(models.MyClass.class_name == name).first()
    if db_myclass:
        return None
    db_myclass = models.MyClass(id=id, class_name=name, numbers=stuNum, joinCode=joinCode)
    db.add(db_myclass)
    db.commit()
    db.refresh(db_myclass)
    return db_myclass


# 获取目标id的班级学生列表
def get_class_list(db: Session, class_id: int) -> List[models.User] | None:
    db_joinclass = db.query(models.JoinClass).filter(models.JoinClass.class_id == class_id).all()
    if not db_joinclass:
        return None
    user_ids = [int(join_class.id) for join_class in db_joinclass]
    return db.query(models.User).filter(models.User.id.in_(user_ids)).all()


# 加入班级
def join_class(id: int, joinCode: str, db: Session) -> int:
    db_myclass = db.query(models.MyClass).filter(models.MyClass.joinCode == joinCode).first()
    if not db_myclass:
        return 0
    if db_myclass.id == id:
        return 2
    if not db.query(models.JoinClass).filter(
            models.JoinClass.id == id , models.JoinClass.class_id == db_myclass.class_id).first():
        db_joinclass = models.JoinClass(id=id, class_id=db_myclass.class_id)
        db.add(db_joinclass)
        db.commit()
        db.refresh(db_joinclass)
        return 1
    return -1


# 删除班级
def delete_class(db: Session, class_id: int) -> int:
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
    db_checkin = db.query(models.checkInRecord).filter(models.checkInRecord.class_id == class_id).all()
    check_in_list = [item.check_in_id for item in db_checkin]
    db_signin = db.query(models.signInRecord).filter(models.signInRecord.check_in_id.in_(check_in_list)).all()
    for signin in db_signin:
        db.delete(signin)
    db.commit()
    for checkin in db_checkin:
        db.delete(checkin)
    db.commit()
    return 1


def StartSign(db: Session, class_id: int, time: int) -> models.checkInRecord:
    db_class = db.query(models.MyClass).filter(models.MyClass.class_id == class_id).first()
    if not db_class:
        return None
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=time)
    numbers = string.digits
    randomNumber = ''.join(choice(numbers) for _ in range(4))
    db_checkIn = models.checkInRecord(id=db_class.id, class_id=class_id,
                                      start_time=start_time, end_time=end_time, signIn_number=randomNumber)

    db.add(db_checkIn)
    db.commit()
    db.refresh(db_checkIn)
    query_result = db.query(models.JoinClass).filter(models.JoinClass.class_id == class_id).all()
    id_result = [item.id for item in query_result]
    for id in id_result:
        db_result = models.signInRecord(check_in_id=db_checkIn.check_in_id, id=id, signIn_status=0)
        db.add(db_result)
        db.commit()
        db.refresh(db_result)
    return db_checkIn


def EndSign(db: Session, checkIn_id: int) -> int:
    db_class = db.query(models.checkInRecord).filter(models.checkInRecord.check_in_id == checkIn_id).first()
    if not db_class:
        return 0
    current_time = datetime.now()
    if current_time > db_class.end_time:
        return -1
    db.query(models.checkInRecord).filter(models.checkInRecord.check_in_id == checkIn_id).update(
        {'end_time': current_time})
    db.commit()
    return 1

def getclassInfo(db:Session, classid: int):
    db_class = db.query(models.MyClass).filter(models.MyClass.class_id == classid).first()
    if not db_class:
        return {}
    grouped_stats = db.query(
        models.JoinClass.class_id,
        func.count(models.JoinClass.id).label('total'),
    ).filter(models.JoinClass.class_id == classid).first()
    return {"class_id":str(db_class.class_id),"class_num":db_class.class_name,"creator_id":db_class.id,
            "total":str(grouped_stats.total)}


def signUp(id: int, class_id: int,  currenttime: DateTime, signIn_number:str,db: Session) -> int:
    db_class = db.query(models.checkInRecord).filter(models.checkInRecord.class_id == class_id).order_by(desc(models.checkInRecord.check_in_id)).first()
    if not db_class:
        return 0
    if not db.query(models.JoinClass).filter(models.JoinClass.id == id, models.JoinClass.class_id == db_class.class_id).first():
        return 0
    print("签到", db_class.signIn_number)
    if db_class.start_time <= currenttime <= db_class.end_time and db_class.signIn_number ==  signIn_number:
        db.query(models.signInRecord).filter(models.signInRecord.id == id,models.checkInRecord.check_in_id == db_class.check_in_id).update({models.signInRecord.signIn_time:currenttime,models.signInRecord.signIn_status:1})
        db.commit()
        return 1
    flag = db.query(models.signInRecord).filter(models.signInRecord.id == id,models.signInRecord.check_in_id == db_class.check_in_id).first()
    if flag.signIn_status == 1:
        return 1
    return 0

def subSign(checkin_id: int, id: int, db: Session) -> int:
    db_signcord = db.query(models.signInRecord).filter(models.signInRecord.id == id, models.signInRecord.check_in_id == checkin_id).first()
    if not db_signcord:
        return 0
    print("签到",db_signcord.check_in_id,  db_signcord.signIn_status)
    if db_signcord.signIn_status == 1 or db_signcord.signIn_status == 2:
        return 2
    elif db_signcord.signIn_status == 0:
        db.query(models.signInRecord).filter(models.signInRecord.id == id , models.signInRecord.check_in_id == checkin_id).update({models.signInRecord.signIn_status:2})
        db.commit()
        return 1
    else:
        return 0

# 删除记录
def del_record(user_id: int, checkin_id: int ,db:Session) -> int:
    db_record = db.query(models.signInRecord).filter(models.signInRecord.id == user_id , models.signInRecord.check_in_id == checkin_id).first()
    if db_record:
        db.delete(db_record)
        db.commit()
        return 1
    return 0

# 获取某次签到记录具体列表
def get_record( checkin_id: int, db:Session):
    db_checkInRecord = db.query(models.checkInRecord).filter(models.checkInRecord.check_in_id == checkin_id).first()
    if not db_checkInRecord:
        return -1
    query_result = db.query(models.signInRecord).filter(models.signInRecord.check_in_id == checkin_id).all()
    id_result = [item.id for item in query_result]
    user_result = db.query(models.User).filter(models.User.id.in_(id_result)).all()
    user_data_dict = {user.id: {"name": user.name} for user in
                      user_result}
    classname = db.query(models.MyClass).filter(models.MyClass.class_id == db_checkInRecord.class_id).first()
    grouped_stats = db.query(
        models.signInRecord.check_in_id,
        func.count(models.signInRecord.id).label('total_records'),
        func.sum(case((models.signInRecord.signIn_status == 0, 1), else_=0)).label('not_signed_in'),
        func.sum(case((models.signInRecord.signIn_status != 0, 1), else_=0)).label('signed_in')
    ).filter(models.signInRecord.check_in_id == checkin_id).first()
    result = []
    for item in query_result:
        user_data = user_data_dict.get(item.id, {})
        result.append(
            {
                **user_data,
                "class": classname.class_name,
                "time": str(item.signIn_time),
                "total": str(grouped_stats.total_records),
                "signed": str(grouped_stats.signed_in),
                "unsigned": str(grouped_stats.not_signed_in),
                "status": str(item.signIn_status)
            }
        )

    return result

# 查询该班级是否存在
def query_class_id(class_id: int, db: Session) -> int:
    if db.query(models.MyClass).filter(models.MyClass.class_id == class_id).first():
        return 1
    return 0


# 查询该班级是否存在签到记录，返回record_id列表/null
def query_record_id(class_id: int, db: Session) -> List[int]:
    record_list = db.query(models.checkInRecord.check_in_id).filter(models.checkInRecord.class_id == class_id).all()
    formatted_list = [item[0] for item in record_list]  # 提取元组中的第一个元素，构建新的列表
    return formatted_list


# 查询record_id对应的学生签到情况
def sign_in_status(status_code):
    if status_code == 2:
        return "已补签"
    elif status_code == 1:
        return "已签到"
    elif status_code == 0:
        return "缺勤"
    else:
        return "未知状态"


# def query_record_message(record_list: [], db: Session) -> List[Dict[str, Any]]:
#     query_result = db.query(models.signInRecord).filter(models.signInRecord.check_in_id.in_(record_list)).all()
#     id_result = [item.id for item in query_result]
#     user_result = db.query(models.User).filter(models.User.id.in_(id_result)).all()
#     user_data_dict = {user.id: {"name": user.name,  "gov_class": user.admin_class} for user in
#                       user_result}
#
#     result = []
#     for item in query_result:
#         user_data = user_data_dict.get(item.id, {})
#         result.append(
#             {
#                 **user_data,
#                 "status": sign_in_status(item.signIn_status),
#                 "id": str(item.check_in_id),
#             }
#         )
#
#     return result

from sqlalchemy import func

def query_record_message(record_list: [], db: Session) -> List[Dict[str, Any]]:
    l = db.query(models.checkInRecord).filter(models.checkInRecord.check_in_id.in_(record_list)).all()
    # 假设 id_list 已经存在并且是 [[check_in_id1, id1], [check_in_id2, id2], ...] 的形式
    list = [[item.check_in_id, item.id] for item in l]
    checkin_list = [item.check_in_id for item in l]
    id_list = [item.id for item in l]
    # 创建一个将 User id 映射到 User name 的字典
    user_dict = {user.id: user.name for user in db.query(models.User).filter(models.User.id.in_(id_list)).all()}
    # print(user_dict,id_list)
    # 构建最终的结果字典
    result_dict = {check_in_id: {"name": user_dict.get(id)} for check_in_id, id in list if
                   id in user_dict}

    # print(result_dict)
    # 获取每个 check_in_id 的签到和未签到人数
    grouped_stats = db.query(
        models.signInRecord.check_in_id,
        func.count(models.signInRecord.id).label('total_records'),
        func.sum(case((models.signInRecord.signIn_status == 0, 1), else_=0)).label('not_signed_in'),
        func.sum(case((models.signInRecord.signIn_status != 0, 1), else_=0)).label('signed_in')
    ).filter(models.signInRecord.check_in_id.in_(checkin_list)).group_by(models.signInRecord.check_in_id)
    result = []
    for item in grouped_stats:
        # print("看这里",item)
        user_data = result_dict.get(item.check_in_id, {})
        result.append(
            {
                **user_data,
                "total": str(item.total_records),
                "signed": str(item.signed_in),
                "unsigned": str(item.not_signed_in),
                "id": item.check_in_id
            }
        )
    return result


def getInfo(id: int, db: Session):
    userinfo = db.query(models.User).filter(models.User.id == id).first()
    return userinfo


def editInfo(id: int, name: str, db: Session):
    db.query(models.User).filter(models.User.id == id).update({models.User.name: name})
    db.commit()
    flag = db.query(models.User).filter(models.User.id == id).first()
    return flag


def get_one_record(id: int, db: Session):
    recordList = db.query(models.signInRecord).filter(models.signInRecord.id == id).all()
    if not recordList:
        return None
    return {"items":[{ "check_in_id": item.check_in_id,
            "signIn_time": str(item.signIn_time),
            "signIn_status": sign_in_status(item.signIn_status)} for item in recordList]}


def get_unsignList(check_in_id: int, db: Session):
    if not db.query(models.checkInRecord).filter(models.checkInRecord.check_in_id == check_in_id,).first():
        return None
    unsignList = db.query(models.signInRecord).filter(models.signInRecord.check_in_id == check_in_id,
                                                      models.signInRecord.signIn_status == 0).all()
    return {"items": [{"id": item.id,
                       "signIn_time": str(item.signIn_time),
                       "signIn_status": sign_in_status(item.signIn_status)} for item in unsignList]}


def get_signList(check_in_id: int, db: Session):
    if not db.query(models.checkInRecord).filter(models.checkInRecord.check_in_id == check_in_id,).first():
        return None
    signList = db.query(models.signInRecord).filter(models.signInRecord.check_in_id == check_in_id,
                                                    models.signInRecord.signIn_status.in_([1,2])).all()
    return {"items":[{ "id": item.id,
            "signIn_time": str(item.signIn_time),
            "signIn_status": sign_in_status(item.signIn_status)} for item in signList]}

