import os

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlmodel import Session

router = APIRouter(
    prefix='',
    tags=['班级']
)
