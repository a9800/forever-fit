from flask import Flask
from flask_login import current_user, login_user, LoginManager, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send
from flask import request
import os

from werkzeug import debug

app = Flask(__name__)
login = LoginManager()



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forever-fit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins=["https://theforever.fit","https://fontawesome.com","https://cdnjs.cloudflare.com","https://ajax.googleapis.com"])

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
    
    socketio.run(app, debug=True)