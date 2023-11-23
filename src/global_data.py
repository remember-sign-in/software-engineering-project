import os
from configparser import ConfigParser

config = ConfigParser()

config.read(os.path.join('config', 'settings.conf'))

# 数据库配置
HOST = config['database']['host']
USER = config['database']['user']
PASSWORD = config['database']['password']


# 小程序配置
APPID = config['app']['appid']
SECRET = config['app']['secret']


