from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["JWT_SECRET_KEY"] = f"{app.config['SECRET_KEY']}"
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://test:password@localhost/test"

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

from app import models
from app import routes

with app.app_context():
    db.create_all()