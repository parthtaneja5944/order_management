from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config import Config
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name = Config):
    app = Flask(__name__)
    app.config.from_object(config_name)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.routes import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/users')

    return app