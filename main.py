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
socketio = SocketIO(app, cors_allowed_origins=["https://theforever.fit"])

if __name__ == "__main__":  
    from routes import *
    from sql_db import *
    login.init_app(app)
    login.login_view = 'Login'

    db.init_app(app)
    @app.before_first_request
    def create_table():
        db.create_all()

    from flask import request
    
    @app.after_request
    def after_request(response):
        white_origin= ["https://kit.fontawesome.com"]
        if request.headers['Origin'] in white_origin:
            response.headers['Access-Control-Allow-Origin'] = request.headers['Origin'] 
            response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response

    @login.user_loader
    def load_user(uname):
        return User.query.get(uname)

    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    socketio.run(app, debug=True)