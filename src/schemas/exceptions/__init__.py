from sqlmodel import SQLModel



BAD_REQUEST_MESSAGE = { 400: { 'model': Response, 'description': '请求错误' } }
FORBIDDEN_MESSAGE = { 401: { 'model': Response, 'description': '没有权限调用该接口' } }
UNAUTHORIZED_MESSAGE = { 403: { 'model': Response, 'description': '未认证' } }
NOT_FOUND_MESSAGE = { 404: { 'model': Response, 'description': '找不到相应的数据' } }
INTERNAL_SERVER_MESSAGE = { 500: { 'model': Response, 'description': '服务端错误' } }