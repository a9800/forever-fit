from flask import Flask
from flask_login import current_user, login_user, LoginManager, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
login = LoginManager()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forever-fit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == "__main__":  
    from routes import *
    from sql_db import *
    login.init_app(app)
    login.login_view = 'Login'

    db.init_app(app)
    @app.before_first_request
    def create_table():
        db.create_all()

    @login.user_loader
    def load_user(uname):
        return User.query.get(uname)

    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    app.run()