from typing import Any
from fastapi import HTTPException, status
from ..responses import Response

class ForbiddenException(HTTPException):
    def __init__(self, headers: dict[str, Any] | None=None) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, Response(code=3, message='没有权限调用该接口').dict(), headers)