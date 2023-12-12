import requests
import uvicorn
from fastapi import Cookie, Depends, FastAPI, responses
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
    return {"test": "测试成功!"}


if __name__ == "__main__":
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000, reload=True)
