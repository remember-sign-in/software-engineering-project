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