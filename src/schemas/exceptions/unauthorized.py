from typing import Any
from fastapi import HTTPException, status
from ..responses import Response

class UserUnauthorizedException(HTTPException):
    def __init__(self, headers: dict[str, Any] | None=None) -> None:
        super().__init__(
            status.HTTP_401_UNAUTHORIZED, 
            Response(code=2, message="用户未认证").dict(),
            headers)

