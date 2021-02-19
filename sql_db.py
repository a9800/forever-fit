from main import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin,db.Model):
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
    id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.String(500))
    room = db.Column(db.String(500))
    date_sent =db.Column(db.String(50))

def user_exits(uname):
    return bool(User.query.filter_by(username=uname).first())

def get_trainers():
    print(User.query.filter_by(isTrainer = True).all())
    return User.query.filter_by(isTrainer = True).all()

if __name__ == "__main__":
    db.create_all()
