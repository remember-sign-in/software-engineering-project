from typing import Any
from fastapi import HTTPException, status
from ..responses import Response

class InternalServerException(HTTPException):
    def __init__(self, msg: str, headers: dict[str, Any] | None=None) -> None:
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, Response(code=1, message=msg).dict(), headers)
