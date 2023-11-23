from typing import Any
from fastapi import HTTPException, status
from ..responses import Response

class BadRequestException(HTTPException):
    def __init__(self, msg: str, headers: dict[str, Any] | None=None) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, Response(code=1, message=msg).dict(), headers)
