from flask.globals import session
from main import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
from sqlalchemy import or_

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(80), unique=True, primary_key=True)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    isTrainer = db.Column(db.Boolean, nullable = False)
    fitnessGoals = db.Column(db.String(120), nullable=True)
    strength = db.Column(db.Boolean, nullable=True)
    endurance = db.Column(db.Boolean, nullable=True)
    mobility = db.Column(db.Boolean, nullable=True)
    combat_sports = db.Column(db.Boolean, nullable=True)
    balance = db.Column(db.Boolean, nullable=True)
    weightloss = db.Column(db.Boolean, nullable=True)
    weightgain = db.Column(db.Boolean, nullable=True)

    sessionsCompleted = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    about = db.Column(db.String(120), nullable=True)

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
    uname = db.Column(db.String(80),db.ForeignKey('user.username'))
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

class Sessions(UserMixin,db.Model):
    __tablename__ = 'upcoming_sessions'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    trainee_username = db.Column(db.String(80),db.ForeignKey('user.username'))
    trainee_fname = db.Column(db.String(80))
    trainee_lname = db.Column(db.String(80))
    trainer_username = db.Column(db.String(80),db.ForeignKey('user.username'))
    trainer_fname = db.Column(db.String(80))
    trainer_lname = db.Column(db.String(80))
    date = db.Column(db.String(120), nullable=False)
    time = db.Column(db.String(120), nullable=False)
    completed =  db.Column(db.Boolean, nullable = False)
    accepted = db.Column(db.Boolean,nullable = False)

class FriendRequest(UserMixin,db.Model):
    __tablename__ = 'friend_requests'
    id = db.Column(db.Integer, primary_key = True)
    requester = db.Column(db.String(80),db.ForeignKey('user.username'))
    requester_fname = db.Column(db.String(80),db.ForeignKey('user.fname'))
    requester_lname = db.Column(db.String(80),db.ForeignKey('user.lname'))
    reciever = db.Column(db.String(80),db.ForeignKey('user.username'))

class Friends(UserMixin,db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer, primary_key = True)
    username_1 = db.Column(db.String(80),db.ForeignKey('user.username'))
    user1_fname = db.Column(db.String(80))
    user1_lname = db.Column(db.String(80))
    username_2 = db.Column(db.String(80),db.ForeignKey('user.username'))
    user2_fname = db.Column(db.String(80))
    user2_lname = db.Column(db.String(80))

class UserTrainer(UserMixin,db.Model):
    __tablename__ = 'user_trainer'
    id = db.Column(db.Integer, primary_key = True)
    trainee_username = db.Column(db.String(80),db.ForeignKey('user.username'))
    trainee_fname = db.Column(db.String(80),db.ForeignKey('user.username'))
    trainee_lname = db.Column(db.String(80),db.ForeignKey('user.username'))
    trainer_username = db.Column(db.String(80),db.ForeignKey('user.username'))
    trainer_fname = db.Column(db.String(80),db.ForeignKey('user.username'))
    trainer_lname = db.Column(db.String(80),db.ForeignKey('user.username'))
    confirmed = db.Column(db.Boolean,nullable = False)

class TrainerReview(UserMixin, db.Model):
    __tablename__ = 'trainer_review'
    id = db.Column(db.Integer, primary_key = True)
    trainee_username = db.Column(db.String(80),db.ForeignKey('user.username'))
    trainee_fname = db.Column(db.String(80),db.ForeignKey('user.username'))
    trainee_lname = db.Column(db.String(80),db.ForeignKey('user.username'))
    trainer_username = db.Column(db.String(80),db.ForeignKey('user.username'))
    rating = db.Column(db.Integer, nullable = False)
    comment = db.Column(db.String(180), nullable = True)


def partnership_exists(user_uname, trainer_uname):
    return bool(UserTrainer.query.filter_by(trainee_username=user_uname,
                                            trainer_username= trainer_uname).first())

def get_trainers_by_trainee(uname):
    return UserTrainer.query.filter_by(trainee_username=uname, confirmed = True).all()

def get_trainees_by_trainer(uname):
    return UserTrainer.query.filter_by(trainer_username=uname, confirmed = True).all()

def get_request_by_trainer(uname):
    return UserTrainer.query.filter_by(trainer_username=uname, confirmed = False).all()

def get_user_trainer(id):
    return UserTrainer.query.filter_by(id=id).first()

def delete_user_trainer(id):
    UserTrainer.query.filter_by(id=id).delete()

def get_user_trainer_trainee(uname1,uname2):
    return UserTrainer.query.filter_by(trainee_username = uname1,trainer_username = uname2 ).first()

def user_exits(uname):
    return bool(User.query.filter_by(username=uname).first())

def get_user(uname):
    return User.query.filter_by(username=uname).first()

def get_trainers():
    return User.query.filter_by(isTrainer = True).all()

def get_clients():
    return User.query.filter_by(isTrainer = False).all()

def filter_get_trainers(filters):
    query = User.query.filter_by(isTrainer = True)
    trainer_types = ['Stength', 'Endurance','Mobility','Combat-Sports','Balance','Weight-Loss','Weight-Gain']
    if 'Strength' in filter:
        query.filter_by(strength = True)
    return query.all()

def room_exists(trainee_uname,trainer_uname):
    return (room_exists_helper(trainee_uname,trainer_uname) or room_exists_helper(trainer_uname,trainee_uname))

def room_exists_helper(uname1,uname2):
    return bool(UserRooms.query.filter_by(trainee_username=uname1,
                                          trainer_username=uname2).first())

def get_room(trainee_uname,trainer_uname):
    if room_exists(trainee_uname,trainer_uname):
        return UserRooms.query.filter_by(trainee_username = trainee_uname, 
                                     trainer_username = trainer_uname).first()

def get_rooms_by_trainee_id(uname):
    return UserRooms.query.filter_by(trainee_username = uname).all()

def get_rooms_by_trainer_id(uname):
    return UserRooms.query.filter_by(trainer_username = uname).all()

def get_limit_rooms_by_trainee_id(uname,limit):
    return UserRooms.query.filter_by(trainee_username = uname).order_by(desc(UserRooms.id)).limit(limit).all()

def get_limit_rooms_by_trainer_id(uname,limit):
    return UserRooms.query.filter_by(trainer_username = uname).order_by(desc(UserRooms.id)).limit(limit).all()

def get_chats():
    return ChatHistory.query.all()

def get_chat_history(room):
    return ChatHistory.query.filter_by(room = room).all()

def friendship_exists(uname1,uname2):
    return (friendship_exists_helper(uname1,uname2) or friendship_exists_helper(uname2,uname1))

def friendship_exists_helper(uname1,uname2):
    return bool(Friends.query.filter_by(username_1 = uname1, 
                                        username_2 = uname2).first())

def friend_request_exists(uname1,uname2):
    return (friend_request_exists_helper(uname1,uname2) or friend_request_exists_helper(uname2,uname1))

def friend_request_exists_helper(uname1,uname2):
    return bool(FriendRequest.query.filter_by(requester = uname1,reciever = uname2).first())

def get_friends(uname):
    return Friends.query.filter(or_(Friends.username_1 == uname, Friends.username_2==uname)).all()

def limit_get_friends(uname,limit):
    return Friends.query.filter(or_(Friends.username_1 == uname, Friends.username_2==uname)).limit(limit).all()

def get_friend_requests(uname):
    return FriendRequest.query.filter_by(reciever = uname).all()

def delete_friend_request(requester,reciever):
    FriendRequest.query.filter_by(requester=requester,reciever=reciever).delete()

def get_session_requests_by_trainerid(uname):
    return Sessions.query.filter_by(trainer_username = uname, accepted = False).all()

def get_sessions_by_trainerid(uname):
    return Sessions.query.filter_by(trainer_username = uname, accepted = True).order_by(Sessions.date).all()

def get_sessions_by_traineeid(uname):
    return Sessions.query.filter_by(trainee_username = uname, accepted = True).order_by(Sessions.date).all()

def get_session_requests_by_id(id):
    return Sessions.query.filter_by(id = id).first()

def get_upcoming_sessions_by_trainee_id(uname,limit):
    return Sessions.query.filter_by(trainee_username = uname).order_by(Sessions.date).limit(limit).all()

def get_upcoming_sessions_by_trainer_id(uname,limit):
    return Sessions.query.filter_by(trainer_username = uname).order_by(Sessions.date).limit(limit).all()

def delete_session(id):
    Sessions.query.filter_by(id = id).delete()

def session_exists(id):
    return bool(Sessions.query.filter_by(id = id).first())

def get_reviews(uname):
    return TrainerReview.query.filter_by(trainer_username = uname).all()

def user_has_highly_rated(uname):
    return bool(TrainerReview.query.filter(TrainerReview.trainee_username == uname,TrainerReview.rating>4).first())

def get_highest_rated_trainer_by_client(uname):
    return TrainerReview.query.filter_by(trainee_username = uname).order_by(TrainerReview.rating).first()

def get_amount_reviews(uname):
    return TrainerReview.query.filter_by(trainer_username = uname).count()

def rating_exists(trainee,trainer):
    return bool(TrainerReview.query.filter_by(trainee_username = trainee, trainer_username = trainer).first())

if __name__ == "__main__":
    db.create_all()
