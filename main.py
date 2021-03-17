from flask import Flask
from flask_login import current_user, login_user, LoginManager, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send
from flask import request
import os

from werkzeug import debug

app = Flask(__name__)
login = LoginManager()

white = ["https://fontawesome.com"]

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
    
    @app.after_request
    def add_cors_headers(response):
        r = request.referrer[:-1]
        if r in white:
            response.headers.add('Access-Control-Allow-Origin', r)
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
            response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
            response.headers.add('Access-Control-Allow-Headers', 'Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        return response

    @login.user_loader
    def load_user(uname):
        return User.query.get(uname)

    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    socketio.run(app, debug=True)