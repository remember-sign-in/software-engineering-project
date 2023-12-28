from data.data import wxappid, wxsecret
import requests
from typing import Any
from datetime import datetime, timedelta
import json


def get_access_token() -> str | None:
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {
        'grant_type': 'client_credential',
        'appid': wxappid,
        'secret': wxsecret
    }
    response_json: dict[str: Any] = requests.get(url, params=params).json()
    print(response_json)
    try:
        response_json['end_time'] = str(datetime.now() + timedelta(seconds=response_json['expires_in']))
        with open('access_token.json', 'w', encoding='utf8') as file:
            json.dump(response_json, file, indent=2)
        return response_json['access_token']
    except Exception as e:
        print(e)
        return None
    

