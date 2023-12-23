type = "mysql+pymysql"

username = "jdqd"
password = "JDQD$520"
ipaddrsss = "rm-cn-wwo3iohzs000cgho.rwlb.rds.aliyuncs.com"
port = 3306
schema = "sztu_jdqd"



SQLALCHEMY_DATABASE_URL = f"{type}://{username}:{password}@{ipaddrsss}:{port}/{schema}"

wxurl = "https://api.weixin.qq.com/sns/jscode2session"
wxappid = "wxe16b90d0fae6e5e9"
wxsecret = "d47821cc3b9abda9c7c7ba7668d0ca2c"