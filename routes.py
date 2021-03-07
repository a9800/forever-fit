from flask import Flask, flash, request, render_template, redirect
from flask_login import current_user, login_user, login_required, logout_user
from form import *
from sql_db import *
from main import app, login, socketio
from flask_socketio import send, join_room, leave_room
from time import localtime, strftime
# pip3 install flask-socketio==4.3.2

@app.route("/")
def home():
    if current_user.is_authenticated:
         return redirect('Home')
    return render_template('index.html')

@app.route('/SignUp')
def SignUp():
    if current_user.is_authenticated:
         return redirect('Home')

    return render_template('signup.html')

@app.route('/SignUpTrainee',methods = ['POST', 'GET'])
def SignUpTrainee():
    if current_user.is_authenticated:
         return redirect('Home')

    if request.method == 'GET':
        return render_template('signup-trainee.html')

    if request.method == 'POST':
        form = request.form
        #print(form)
        if (user_exits(form['username'])):
            flash("Username '"+form['username']+"' is taken")
            return redirect('SignUpTrainee')
        
        else:
            # Changing goals from csv to array
            goals = form['goals'].split(",")
            # Removing empty elemets and sorting it alphabetically
            goals = sorted([i for i in goals if i])

            register = User(username = form['username'], fname = form['fname'],
                            lname = form['lname'], dob = form['birthday'], isTrainer = False,
                            fitnessGoals = form['goals'])
                            
            register.set_password(form['psw'])
            db.session.add(register)
            db.session.commit()
            return redirect('Login')
        
@app.route('/SignUpTrainer',methods = ['POST', 'GET'])
def SignUpTrainer():
    if current_user.is_authenticated:
         return redirect('Home')

    if request.method == 'GET':
        return render_template('signup-trainer.html')

    if request.method == 'POST':
        form = request.form
        #print(form)
        if (user_exits(form['username'])):
            flash("Username '"+form['username']+"' is taken")
            return redirect('SignUpTrainer')
        
        else:
            # Changing goals from csv to array
            goals = form['goals'].split(",")
            # Removing empty elemets and sorting it alphabetically
            goals = sorted([i for i in goals if i])

            #print(goals)
            register = User(username = form['username'], fname = form['fname'],
                            lname = form['lname'], dob = form['birthday'], isTrainer = True,
                            fitnessGoals = form['goals'])

            register.set_password(form['psw'])
            db.session.add(register)
            db.session.commit()
            return redirect('Login')

@app.route('/Login',methods = ['POST','GET'])
def Login():
    if current_user.is_authenticated:
        return redirect('Home')
     
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username = username).first()
        
        if user is not None and user.check_password(request.form['psw']):
            login_user(user)
            return redirect('Home')
     
    return render_template('login.html')

@app.route('/Home')
@login_required
def Home():
    if(not current_user.isTrainer):
        friends = limit_get_friends(current_user.username,5)
        recent_rooms = get_limit_rooms_by_trainee_id(current_user.username,2)
        upcoming_sessions = get_upcoming_sessions_by_trainee_id(current_user.username,2)
        return render_template('home.html',recent_rooms=recent_rooms,friends=friends,upcoming_sessions=upcoming_sessions)
    else:
        recent_rooms = get_limit_rooms_by_trainer_id(current_user.username,2)
        upcoming_sessions = get_upcoming_sessions_by_trainer_id(current_user.username,2)
        return render_template('trainer-home.html',recent_rooms=recent_rooms, upcoming_sessions=upcoming_sessions)

@app.route('/TrainerSearch')
@login_required
def TrainerSearch():
    return render_template('trainer-search.html', trainers = get_trainers())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/chats')
@login_required
def chats():
    if(not current_user.isTrainer):
        ROOMS = get_rooms_by_trainee_id(current_user.username)

        return render_template('chats.html', curr_uname = current_user.username, is_trainer = current_user.isTrainer,
                                curr_fname = current_user.fname, curr_lname = current_user.lname, 
                                rooms=ROOMS)
    else:
        
        ROOMS = get_rooms_by_trainer_id(current_user.username)

        return render_template('chats.html', curr_uname = current_user.username, is_trainer = current_user.isTrainer,
                                curr_fname = current_user.fname, curr_lname = current_user.lname, 
                                rooms=ROOMS)



@app.route('/chat/<uname>')
@login_required
def sessions(uname):
    if(not current_user.isTrainer):
        if(not room_exists(current_user.username, uname)):
            room = UserRooms(trainee_username= current_user.username,
                             trainee_fname = current_user.fname,
                             trainee_lname = current_user.lname,
                             trainer_username = uname,
                             trainer_fname = get_user(uname).fname,
                             trainer_lname = get_user(uname).lname)
            db.session.add(room)
            db.session.commit()
            ROOMS = get_rooms_by_trainee_id(current_user.username)
        else:
            ROOMS = get_rooms_by_trainee_id(current_user.username)

        curr_room = get_room(current_user.username, uname)

        messages = get_chat_history(curr_room.id)

        partnership = partnership_exists(current_user.username,uname)

        return render_template('session.html',uname = uname, curr_uname = current_user.username,
                                curr_fname = current_user.fname, curr_lname = current_user.lname, 
                                rooms=ROOMS, messages = messages, curr_room = curr_room,
                                partnership=partnership)
    else:
        if(room_exists(uname, current_user.username)):
            ROOMS = get_rooms_by_trainer_id(current_user.username)

        curr_room = get_room(uname, current_user.username)

        messages = get_chat_history(curr_room.id)

        partnership = partnership_exists(uname,current_user.username)

        return render_template('trainer-session.html',uname = uname, curr_uname = current_user.username,
                                curr_fname = current_user.fname, curr_lname = current_user.lname, 
                                rooms=ROOMS, messages = messages, curr_room = curr_room,
                                partnership=partnership)

@socketio.on('message')
def message(data):
    #print(data['room_id'])
    message = ChatHistory(message=data['msg'],
                          room=data['room_id'], 
                          uname = current_user.username,
                          fname = current_user.fname,
                          lname = current_user.lname,
                          date_sent=strftime('%b-%d %I:%M%p',localtime()))
    db.session.add(message)
    db.session.commit()

    send({'msg': data['msg'], 'uname': data['uname'], 'fname': data['fname'], 'lname': data['lname']
          ,'time_stamp':strftime('%b-%d %I:%M%p',localtime())},
          room = data['room_id'])


@app.route('/TrainingSessions')
@login_required
def training_sessions():
    if current_user.isTrainer:
        trainers = get_trainees_by_trainer(current_user.username)
        requests = get_session_requests_by_trainerid(current_user.username)
        sessions = get_sessions_by_trainerid(current_user.username)
        return render_template('training-sessions.html', current_user = current_user, trainers = trainers, requests = requests,
                                sessions = sessions)
    else:
        trainers = get_trainers_by_trainee(current_user.username)
        sessions = get_sessions_by_traineeid(current_user.username)
        return render_template('training-sessions.html', current_user = current_user, trainers = trainers, sessions = sessions)

@app.route('/BookSession/<uname>',methods=['POST','GET'])
@login_required
def book_session(uname):
    if request.method == 'GET':
        if current_user.isTrainer:
            return redirect('/Home')
        else:
            return render_template('book-session.html',trainer=get_user(uname))
    
    if request.method == 'POST':
        form = request.form
        session = Sessions(
                    trainee_username = current_user.username,
                    trainee_fname = current_user.fname,
                    trainee_lname = current_user.lname,
                    trainer_username = uname,
                    trainer_fname = get_user(uname).fname,
                    trainer_lname = get_user(uname).lname,
                    date = form['date'],
                    time = form['time'],
                    completed = False,
                    accepted = False
        )
        db.session.add(session)
        db.session.commit()
        flash('You have sent '+get_user(uname).fname+' a session request')
        return redirect('/TrainingSessions')

@app.route('/session_accept/<id>')
@login_required
def session_accept(id):
    session = get_session_requests_by_id(id)
    session.accepted = True
    db.session.commit()
    return redirect('/TrainingSessions')

@app.route('/session_deny/<id>')
@login_required
def session_deny(id):
    delete_session_request(id)
    return redirect('/TrainingSessions')
    
@socketio.on('join')
def join(data):
    #print(data['room_name'])
    join_room(data['room'])
    #send({'msg':data['uname'] + " has joined the " + data['room_name'] + " room."},
    #      room=data['room']
    #     )

@socketio.on('leave')
def leave(data):

    leave_room(data['room_name'])
    #send({'msg': data['uname'] +" has left the " + data['room_name'] + " room."},
    #      room=data['room']
    #     )

@app.route('/Friends', methods = ['POST','GET'])
@login_required
def friends():
    if request.method == 'GET':
        if(not current_user.isTrainer):
            requests = get_friend_requests(current_user.username)
            friends = get_friends(current_user.username)
            return render_template('friends.html',requests = requests,user=current_user.username,friends=friends)
        else:
            return redirect('Home')
    
    if request.method == 'POST':
        form = request.form
        #print('\n\n\n'+form['uname']+'\n\n\n')
        
        if not user_exits(form['uname']):
            flash(form['uname']+' Is not a valid username')
            return redirect('Friends')

        elif get_user(form['uname']).isTrainer:
            flash('User '+form['uname']+' is not a Trainee, You can only send friend requests to trainees')
            return redirect('Friends')

        elif friendship_exists(current_user.username, form['uname']):
            flash('User '+form['uname']+' is already your friend')
            return redirect('Friends')

        elif friend_request_exists(current_user.username,form['uname']):
            flash('You or user '+ form['uname'] + " have already sent a friend request to each other")
            return redirect('Friends')

        else:
            req = FriendRequest(requester = current_user.username,
                                requester_fname = current_user.fname,
                                requester_lname = current_user.lname,
                                reciever = form['uname'])

            db.session.add(req)
            db.session.commit()
            flash('You have sent '+form['uname']+' a friend request')
            
            return redirect('Friends')

@app.route('/friend_accept/<uname>')
@login_required
def friend_accept(uname):
    if friend_request_exists(uname,current_user.username):
        delete_friend_request(uname,current_user.username)
        friendship = Friends(
            username_1 = current_user.username,
            user1_fname = current_user.fname,
            user1_lname = current_user.lname,
            username_2 = uname,
            user2_fname = get_user(uname).fname,
            user2_lname = get_user(uname).lname
        )
        db.session.add(friendship)
        db.session.commit()

        return redirect('/Friends')
    else:
        return redirect('/Friends')

@app.route('/friend_deny/<uname>')
@login_required
def friend_deny(uname):
    if friend_request_exists(uname,current_user.username):
        delete_friend_request(uname,current_user.username)

        return redirect('/Friends')
    else:
        return redirect('/Friends')

@app.route('/addTrainer/<trainer_username>')
@login_required
def addTrainer(trainer_username):
    if current_user.isTrainer:
        return redirect('Home')
    else:
        if not partnership_exists(current_user.username,trainer_username):
            user_trainer = UserTrainer(trainee_username = current_user.username,
                                       trainee_fname = current_user.fname,
                                       trainee_lname = current_user.lname,
                                       trainer_username = trainer_username,
                                       trainer_fname = get_user(trainer_username).fname,
                                       trainer_lname = get_user(trainer_username).lname)
            db.session.add(user_trainer)
            db.session.commit()
            return redirect('/chat/'+trainer_username)
