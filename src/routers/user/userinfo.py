# -*- coding : utf8 -*-
# coding : unicode_escape

from fastapi import APIRouter, Depends
from sqlmodel import Session


router = APIRouter(
    prefix='/info',
    tags=['用户信息']
    )
