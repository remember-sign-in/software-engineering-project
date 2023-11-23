from sqlmodel import create_engine



DATABASE_URL = ''

engine = create_engine(DATABASE_URL, encoding='utf8', echo=True, pool_recycle=3600)
