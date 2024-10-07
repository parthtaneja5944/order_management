import os

class Config:
    JWT_SECRET_KEY  = 'dab8052cc2c992749dcea05a288227706fc0a8d790d9637ce431243356438424'
    SQLALCHEMY_DATABASE_URI = 'postgresql://user_model_admin:user_model_admin@user_db:5432/user_model'
    SQLALCHEMY_TRACK_MODIFICATIONS = False