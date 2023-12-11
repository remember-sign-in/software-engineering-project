type = "mysql+pymysql"

username = "jdqd"
password = "JDQD$520"
ipaddrsss = "rm-cn-wwo3iohzs000cgho.rwlb.rds.aliyuncs.com"
port = 3306
schema = "sztu_jdqd"


SQLALCHEMY_DATABASE_URL = f"{type}://{username}:{password}@{ipaddrsss}:{port}/{schema}"

wxurl = "https://api.weixin.qq.com/sns/jscode2session"
wxappid = "wxe16b90d0fae6e5e9"
wxsecret = "c4824ebe59357e31272513763ed7d5f8"