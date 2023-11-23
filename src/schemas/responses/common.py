from enum import IntEnum
from typing import Optional

from sqlmodel import Field, SQLModel


class StatusCode(IntEnum):
    SUCCESS = 0

class Response(SQLModel):
    code: int = Field(..., description='返回状态码')
    message: str = Field(..., description='返回状态注释')

class watermark(SQLModel):
    appid: str = Field(..., description='小程序appid')
    timestamp: int = Field(..., description='用户获取手机号操作的时间戳')

class phone_info(SQLModel):
    phoneNumber: str = Field(..., description='用户绑定的手机号（国外手机号会有区号）')
    purePhoneNumber: str = Field(..., description='没有区号的手机号')
    countryCode: str = Field(..., description='区号')
    watermark: Optional[watermark]

class PhoneResponse(SQLModel):
    errcode: int = Field(..., description='错误码')
    errmsg: str = Field(..., description='错误提示信息')
    phone_info: Optional[phone_info]

