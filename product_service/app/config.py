import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://product_model_admin:product_model_admin@product_db:5432/product_model'
    SQLALCHEMY_TRACK_MODIFICATIONS = False