# -*- coding : utf8 -*-
# coding : unicode_escape
import os
from time import sleep

from fastapi import APIRouter, Depends
from sqlmodel import Session

router = APIRouter(
    prefix='',
    tags=['签到']
)
