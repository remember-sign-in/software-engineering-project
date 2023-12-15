from datetime import datetime

import requests
import uvicorn
from fastapi import Cookie, Depends, FastAPI, responses
from sqlalchemy import DateTime

import crud, models, schemas
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from data.data import wxappid, wxsecret, wxurl

# 在数据库中生成表结构
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 连接数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/api/JDQD/getOpenid",
    response_model=schemas.User,
    summary="用户微信登录",
    description="通过用户传入的验证码，借助微信提供的api获取到用户id并进行登录",
    tags=["用户身份认证"],
)
def getid(code: str, db: Session = Depends(get_db)):
    params = {
        "appid": wxappid,
        "secret": wxsecret,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    # 访问微信api，获取openid(用户唯一标识)--登录凭证校验
    data = requests.get(wxurl, params=params).json()
    print(data)
    if "openid" not in data:
        resp = responses.JSONResponse(content=data)
        print("no openid")
        return resp

    openid = data["openid"]
    print(data)
    db_user = crud.get_user_by_openid(db, openid)
    if not db_user:
        db_user = crud.create_user(db=db, openid=openid)

    resp = responses.JSONResponse(content={"id": db_user.id})
    resp.set_cookie(key="openid", value=openid)
    return resp


@app.get("/test")
def test():
    return {"msg": "hello worlddddddd!!!!"}


@app.get("/home/createList/{id}")
async def getMyClass(id: str, db: Session = Depends(get_db)):
    db_myclass = crud.get_my_class(db, id)
    if not db_myclass:
        return responses.JSONResponse(content={"items": "null"})
    return responses.JSONResponse(content={"items": [
        {"index": db_myclass.class_id, "joinCode": db_myclass.joinCode, "numbers": db_myclass.numbers,
         "name": db_myclass.class_name, "id": db_myclass.user_id}]})


@app.get("/home/joinList/{id}")
async def getJoinClass(id: str, db: Session = Depends(get_db)):
    db_joinclass = crud.get_join_class(db, id)
    if not db_joinclass: return responses.JSONResponse(content={"items": "null"})
    return responses.JSONResponse(content={"items": [
        {"index": db_joinclass.class_id, "joinCode": db_joinclass.joinCode, "numbers": db_joinclass.numbers,
         "name": db_joinclass.class_name, "id": db_joinclass.user_id}]})


@app.post("/class/create_class")
async def createClass(creator_id: str, name: str, joinCode: str, stuNum: int, db: Session = Depends(get_db)):
    db_myclass = crud.create_class(db, creator_id, name, joinCode, stuNum)
    return responses.JSONResponse(content={
        "message": [{"班级id": db_myclass.class_id, "班级名称": db_myclass.class_name, "result": "创建班级成功"}]})


@app.get("/class/classList/{id}")
async def getClassLsit(id: str, db: Session = Depends(get_db)):
    # id 为class_id
    db_user = crud.get_class_list(db, id)
    if not db_user: return responses.JSONResponse(content={"items": "null"})
    return responses.JSONResponse(
        content={"name": db_user.name, "gov_class": db_user.admin_class, "id": db_user.id})


@app.post("/class/joinClass")
async def joinClass(id: str, joinCode: str, db: Session = Depends(get_db)):
    flag = crud.join_class(db, id, joinCode)
    if flag == 0:
        return responses.JSONResponse(content={"message": [{"学生id": id, "result": "加入班级失败"}]})
    elif flag == 1:
        return responses.JSONResponse(content={"message": [{"学生id": id, "result": "加入班级成功"}]})
    else:
        return responses.JSONResponse(content={"message": [{"学生id": id, "result": "已经加入过此班级"}]})


@app.delete("/class/deleteClass/{class_id}")
async def deleteClass(class_id: str, db: Session = Depends(get_db)):
    db_state = crud.delete_class(db, class_id)
    return responses.JSONResponse(content={"state": db_state})


@app.post("/user/startSign")
async def start_sign(user_id: str, class_id: str, starttime: datetime, db: Session = Depends(get_db())):
    flag = crud.startsign(db, user_id, class_id, starttime)
    if flag == 1:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "发起签到成功！"}]})
    else:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "发起签到失败！"}]})

@app.post("/user/endSign")
async def start_sign(user_id: str, class_id: str, endtime: datetime, db: Session = Depends(get_db())):
    flag = crud.startsign(db, user_id, class_id, endtime)
    if flag == 1:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "结束签到成功！"}]})
    else:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "结束签到失败！"}]})
# @app.get("/record/list")
# async def get_list(db: Session = Depends(get_db())):
#     pass
#
#
# @app.get("/record/detail")
# async def get_record(db: Session = Depends(get_db())):
#     pass
#
#
# @app.get("/record/oneRecord")
# async def get_oneRedcord(db: Session = Depends(get_db())):
#     pass
#
#
# @app.get("/record/unsignList")
# async def get_unsignlist(db: Session = Depends(get_db())):
#     pass
#
#
# @app.get("/record/signList")
# async def get_signlist(db: Session = Depends(get_db())):
#     pass
#
#
# @app.delete("/record/del")
# async def del_record(db: Session = Depends(get_db())):
#     pass


if __name__ == "__main__":
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)
