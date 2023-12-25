from datetime import datetime
import json
import requests
import uvicorn
from fastapi import Cookie, Depends, FastAPI, responses
from sqlalchemy import DateTime
from requests.exceptions import ConnectTimeout
from pydantic import BaseModel
import crud, models, schemas
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from data.data import wxappid, wxsecret, wxurl, template_id
from message import get_access_token
# 在数据库中生成表结构

# models.Base.metadata.create_all(bind=engine)

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
    # wxurl = f"{wxurl}?appid={wxappid}&secret={wxsecret}&js_code={code}&grant_type=authorization_code"
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
    resp = responses.JSONResponse(content={"token": db_user.open_id, "id": db_user.id})
    return resp


@app.get("/test")
def test():
    return {"test": "服务器连接正常!"}


@app.get("/home/createList/{id}")
async def getMyClass(id: int, db: Session = Depends(get_db)):
    db_myclass = crud.get_my_class(db, id)
    if not db_myclass:
        return responses.JSONResponse(content={"items": "null"})
    return responses.JSONResponse(content={"items": [
        {"index": item.class_id, "joinCode": item.joinCode, "numbers": item.numbers,
         "name": item.class_name, "id": item.id} for item in db_myclass]})


@app.get("/home/joinList/{id}")
async def getJoinClass(id: int, db: Session = Depends(get_db)):
    db_joinclass = crud.get_join_class(db, id)
    if not db_joinclass:
        return responses.JSONResponse(content={"items": "null"})
    result = responses.JSONResponse(content={"items": [
        {"index": item.class_id, "joinCode": item.joinCode, "numbers": str(item.numbers),
         "name": item.class_name, "id": item.id} for item in db_joinclass]})
    return result


@app.get("/home/searchList")
async def searchList(class_name: str, db: Session = Depends(get_db)):
    db_searchclass = crud.get_search_class(class_name, db)
    if not db_searchclass:
        return responses.JSONResponse(content={"items": "null"})
    result = responses.JSONResponse(content={"items": [
        {"index": item.class_id, "name": item.class_name, "id": item.id} for item in db_searchclass]})
    return result


@app.put("/class/exitClass/{id}")
async def exitClass(id: int, class_id: int, db: Session = Depends(get_db)):
    db_exitclass = crud.exit_class(id, class_id, db)
    if db_exitclass == -1:
        return responses.JSONResponse(content={"id": id, "result": "本就不在此班级！"})
    else:
        return responses.JSONResponse(content={"id": id, "result": "成功退出此班级！"})


@app.put("/class/kickClass/{id}")
async def kickClass(id: int, class_id: int, db: Session = Depends(get_db)):
    db_kick_id = crud.kick_class(id, class_id, db)
    if db_kick_id == -1:
        return responses.JSONResponse(content={"student_id": id, "result": "本就不在此班级！"})
    else:
        return responses.JSONResponse(content={"student_id": id, "result": "成功踢出此班级！"})


@app.post("/class/create_class")
async def createClass(id: int, class_name: str, numbers: int, joinCode: int, db: Session = Depends(get_db)):
    db_myclass = crud.create_class(id, class_name, joinCode,
                                   numbers, db)
    if not db_myclass:
        return responses.JSONResponse(content={
            "message": [{"班级id": "null", "班级名称": "null", "result": "JoinCode已被其他班级使用"}]})
    return responses.JSONResponse(content={
        "message": [{"班级id": db_myclass.class_id, "班级名称": db_myclass.class_name, "result": "创建班级成功"}]})


@app.get("/class/classList/{id}")
async def getClassLsit(id: int, db: Session = Depends(get_db)):
    # id 为class_id
    db_user = crud.get_class_list(db, id)
    if not db_user:
        return responses.JSONResponse(content={"items": "null"})
    return responses.JSONResponse(
        content={[{"name": item.name, "gov_class": item.admin_class, "id": item.id} for item in db_user]})


@app.post("/class/joinClass")
async def joinClass(id: int, joinCode: str, db: Session = Depends(get_db)):
    flag = crud.join_class(id, joinCode, db)
    if flag == 0:
        return responses.JSONResponse(content={"info": "加入班级失败"})
    elif flag == 1:
        return responses.JSONResponse(content={"info": "加入班级成功"})
    else:
        return responses.JSONResponse(content={"info": "已经加入过此班级"})


@app.delete("/class/deleteClass/{class_id}")
async def deleteClass(class_id: int, db: Session = Depends(get_db)):
    db_state = crud.delete_class(db, class_id)
    return responses.JSONResponse(content={"state": db_state})


@app.post("/user/startSign")
async def start_sign(id: int, class_id: int, starttime: datetime, endtime: datetime,
                     db: Session = Depends(get_db)):
    flag = crud.StartSign(db, id, class_id, starttime, endtime)
    if flag == 1:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "发起签到成功！"}]})
    else:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "发起签到失败！"}]})


@app.post("/user/endSign")
async def end_sign(id: int, class_id: int, db: Session = Depends(get_db)):
    current_time = datetime.now()
    flag = crud.EndSign(db, id, class_id, current_time)
    if flag == 1:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "结束签到成功！"}]})
    elif flag == 2:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "签到已经结束！"}]})
    else:
        return responses.JSONResponse(content={"message": [{"班级id": class_id, "result": "结束签到失败！"}]})


@app.post("/user/signUp")
async def sign_up(id: int, class_id: int, db: Session = Depends(get_db)):
    current_time = datetime.now()
    flag = crud.signUp(id, class_id, db, current_time)
    if flag == 1:
        return responses.JSONResponse(content={"message": [{"用户id": id, "result": "签到成功！"}]})
    else:
        return responses.JSONResponse(content={"message": [{"用户id": id, "result": "签到失败！"}]})


@app.post("/user/subSign")
async def sub_sign(check_id: int, id: int, db: Session = Depends(get_db)):
    flag = crud.subSign(check_id, id, db)
    if flag == 1:
        return responses.JSONResponse(content={"message": [{"用户id": id, "result": "补签成功！"}]})
    elif flag == 2:
        return responses.JSONResponse(content={"message": [{"用户id": id, "result": "已经签到！"}]})
    else:
        return responses.JSONResponse(content={"message": [{"用户id": id, "result": "补签失败！"}]})


@app.post("/user/regist")
async def regist(open_id: str, name: str, admin_class: str, username: str, password: str,
                 db: Session = Depends(get_db)):
    db_user = crud.create_user(open_id, name, admin_class, username, password, db)
    if db_user is not None:
        return responses.JSONResponse(content={"message": "注册成功！"})
    else:
        return responses.JSONResponse(content={"message": "注册失败！"})


@app.get("/user/login")
async def login(username: str, password: str, db: Session = Depends(get_db)) -> int:
    db_login = crud.login_user(username, password, db)
    if db_login is None:
        return responses.JSONResponse(content={"message": "登录成功！"})
    else:
        return responses.JSONResponse(content={"message": "登录失败！"})

@app.get("/record/list/{id}")
async def get_recordlist(id: int, db: Session = Depends(get_db)):
    '''
    1.查询“创建班级"表判断class_id是否存在，不存在该班级，返回{}
    2.查询“发起签到"表根据class_id记录record_id，如果record_id为空，不存在签到活动，返回{}
    3.查询"签到记录"表根据record_id记录user_id,status,record_id
    4.查询"用户"表根据user_id记录name,number,gov_class
    5.最终返回name,number,gov_class,status,record_id
    '''
    print(id)
    if crud.query_class_id(id,db) == 0:
        return responses.JSONResponse(content={"info":"该班级不存在","name": "","number": "","gov_class": "","status": "","id": ""})
    db_record_list = crud.query_record_id(id,db)
    if not db_record_list:
        return responses.JSONResponse(content={"info":"该班级还未存在签到记录","name": "","number": "","gov_class": "","status": "","id": ""})
    list = crud.query_record_message(db_record_list,db)
    return responses.JSONResponse(content=[item for item in list])


class PushResponse(BaseModel):
    errcode: int
    errmsg: str


@app.post('/user/msgpush/')
def send_received_message_to_user(db: Session=Depends(get_db)):

    url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send'

    params = {
        'access_token': get_access_token()
    }

    headers = {
        'content-type': 'text/plain'
    }

    data = {
        'touser': "oqLDB5C0eFW9gFXBljsw53yypJTU",
        'template_id': template_id,
        'miniprogram_state': 'developer',
        'data': {
            'name1': {
                'value': "name1"
            },
            'time2': {
                'value': "time2"
            },
            'phrase4': {
                'value': "phrase4"
            },
            'thing5': {
                'value': "thing5"
            },
        }
    }
    try:
        response = requests.post(url, params=params, data=json.dumps(data), headers=headers, timeout=5)
        data = response.json()
        print(data)
        pushresponse = PushResponse(errcode=data['errcode'],errmsg=data['errmsg'])
        return pushresponse
    except ConnectTimeout:
        print('微信服务器出了些小问题')

if __name__ == "__main__":
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000, reload=True)
