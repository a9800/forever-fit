from main import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(80), unique=True, primary_key=True)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    isTrainer = db.Column(db.Boolean, nullable = False)
    fitnessGoals = db.Column(db.String(120), nullable=True)

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
           return (self.username)

class ChatHistory(UserMixin,db.Model):
    __tablename__ = 'chat_history'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    message = db.Column(db.String(500))
    room = db.Column(db.String(500))
    date_sent = db.Column(db.String(50))
    fname = db.Column(db.String(80),db.ForeignKey('user.fname'))
    lname = db.Column(db.String(80),db.ForeignKey('user.lname'))

class UserRooms(UserMixin,db.Model):
    __tablename__ = 'user_rooms'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    trainee_username = db.Column(db.String(80),db.ForeignKey('user.username'))
    trainee_fname = db.Column(db.String(80))
    trainee_lname = db.Column(db.String(80))
    trainer_username = db.Column(db.String(80),db.ForeignKey('user.username'))
    trainer_fname = db.Column(db.String(80))
    trainer_lname = db.Column(db.String(80))

def user_exits(uname):
    return bool(User.query.filter_by(username=uname).first())

def get_user(uname):
    return User.query.filter_by(username=uname).first()

def get_trainers():
    print(User.query.filter_by(isTrainer = True).all())
    return User.query.filter_by(isTrainer = True).all()

def room_exists(trainee_uname,trainer_uname):  
    return bool(UserRooms.query.filter_by(trainee_username=trainee_uname,
                                          trainer_username=trainer_uname).first())

def get_room(trainee_uname,trainer_uname):
    if room_exists(trainee_uname,trainer_uname):
        return UserRooms.query.filter_by(trainee_username = trainee_uname, 
                                     trainer_username = trainer_uname).first()

def get_rooms_by_trainee_id(uname):
    return UserRooms.query.filter_by(trainee_username = uname).all()

def get_chats():
    return ChatHistory.query.all()

def get_chat_history(room):
    return ChatHistory.query.filter_by(room = room).all()

if __name__ == "__main__":
    db.create_all()
