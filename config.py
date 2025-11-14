import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')   # ganti dengan yang aman
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES =60 
    SQLALCHEMY_DATABASE_URI = os.getenv('SQL_URI')
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 5,
        'max_overflow': 5,
        'pool_timeout': 30
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_AI=os.getenv('API_AI')
