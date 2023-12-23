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
        {"index": item.class_id, "joinCode": item.joinCode, "numbers": item.numbers,
         "name": item.class_name, "id": item.creator_id} for item in db_myclass]})


@app.get("/home/joinList/{id}")
async def getJoinClass(id: str, db: Session = Depends(get_db)):
    db_joinclass = crud.get_join_class(db, id)
    if not db_joinclass:
        return responses.JSONResponse(content={"items": "null"})
    result = responses.JSONResponse(content={"items": [
        {"index": item.class_id, "joinCode": item.joinCode, "numbers": str(item.numbers),
         "name": item.class_name, "id": item.creator_id}] for item in db_joinclass})
    print(result)
    return result


@app.put("/class/exitClass/{id}")
async def exitClass(id: str, class_id: str, db: Session = Depends(get_db)):
    db_exitclass = crud.exit_class(id, class_id, db)
    if db_exitclass == -1:
        return responses.JSONResponse(content={"user_id": id, "result": "本就不在此班级！"})
    else:
        return responses.JSONResponse(content={"user_id": id, "result": "成功退出此班级！"})


@app.put("/class/kickClass/{id}")
async def kickClass(id: str, class_id: str, db: Session = Depends(get_db)):
    db_kick_id = crud.kick_class(id, class_id, db)
    if db_kick_id == -1:
        return responses.JSONResponse(content={"student_id": id, "result": "本就不在此班级！"})
    else:
        return responses.JSONResponse(content={"student_id": id, "result": "成功踢出此班级！"})


@app.post("/class/create_class")
async def createClass(creator_id: str, class_name: str, numbers: int, joinCode: int, db: Session = Depends(get_db)):
    db_myclass = crud.create_class(creator_id, class_name, joinCode,
                                   numbers, db)
    if not db_myclass:
        return responses.JSONResponse(content={
            "message": [{"班级id": "null", "班级名称": "null", "result": "JoinCode已被其他班级使用"}]})
    return responses.JSONResponse(content={
        "message": [{"班级id": db_myclass.class_id, "班级名称": db_myclass.class_name, "result": "创建班级成功"}]})


@app.get("/class/classList/{id}")
async def getClassLsit(id: str, db: Session = Depends(get_db)):
    # id 为class_id
    db_user = crud.get_class_list(db, id)
    if not db_user:
        return responses.JSONResponse(content={"items": "null"})
    return responses.JSONResponse(
        content={[{"name": item.name, "gov_class": item.admin_class, "id": item.user_id}] for item in db_user})


@app.post("/class/joinClass")
async def joinClass(student_id: str, joinCode: str, db: Session = Depends(get_db)):
    flag = crud.join_class(student_id, joinCode, db)
    if flag == 0:
        return responses.JSONResponse(content={"info": "加入班级失败"})
    elif flag == 1:
        return responses.JSONResponse(content={"info": "加入班级成功"})
    else:
        return responses.JSONResponse(content={"info": "已经加入过此班级"})


@app.delete("/class/deleteClass/{class_id}")
async def deleteClass(class_id: str, db: Session = Depends(get_db)):
    db_state = crud.delete_class(db, class_id)
    return responses.JSONResponse(content={"state": db_state})


@app.post("/user/startSign")
async def start_sign(user_id: str, class_id: str, starttime: datetime, endtime: datetime,
                     db: Session = Depends(get_db)):
    flag = crud.StartSign(db, user_id, class_id, starttime, endtime)
    if flag == 1:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "发起签到成功！"}]})
    else:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "发起签到失败！"}]})


@app.post("/user/endSign")
async def end_sign(user_id: str, class_id: str, db: Session = Depends(get_db)):
    current_time = datetime.now()
    flag = crud.EndSign(db, user_id, class_id, current_time)
    if flag == 1:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "结束签到成功！"}]})
    elif flag == 2:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "签到已经结束！"}]})
    else:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "结束签到失败！"}]})


@app.post("/user/signUp")
async def sign_up(user_id: str, class_id: str, db: Session = Depends(get_db)):
    current_time = datetime.now()
    flag = crud.signUp(user_id, class_id, db, current_time)
    if flag == 1:
        return responses.JSONResponse(content={"message": [{"用户id": user_id, "result": "签到成功！"}]})
    else:
        return responses.JSONResponse(content={"message": [{"用户id": user_id, "result": "签到失败！"}]})


@app.post("/user/subSign")
async def sub_sign(check_id: str, student_id: str, db: Session = Depends(get_db)):
    flag = crud.subSign(check_id, student_id, db)
    if flag == 1:
        return responses.JSONResponse(content={"message": [{"用户id": student_id, "result": "补签成功！"}]})
    elif flag == 2:
        return responses.JSONResponse(content={"message": [{"用户id": student_id, "result": "已经签到！"}]})
    else:
        return responses.JSONResponse(content={"message": [{"用户id": student_id, "result": "补签失败！"}]})


if __name__ == "__main__":
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000, reload=True)
