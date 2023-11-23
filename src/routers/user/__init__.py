from fastapi import APIRouter, Depends
from sqlmodel import Session


router = APIRouter(
    prefix='/user',
    tags=['用户']
)
