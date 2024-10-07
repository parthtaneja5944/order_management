import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://order_model_admin:order_model_admin@order_db:5432/order_model'
    SQLALCHEMY_TRACK_MODIFICATIONS = False