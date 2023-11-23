import json
from hashlib import sha1


from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix='',
    tags=[''],
    responses=""
)
router.include_router()
