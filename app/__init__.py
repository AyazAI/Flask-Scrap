from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Creating app instance
app = Flask(__name__)
app.config.from_object(Config)

#Initializing DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

