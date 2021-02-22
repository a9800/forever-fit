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
        print(form)
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
        return render_template('signup-trainer.html',form=RegisterForm())

    if request.method == 'POST':
        form = request.form
        print(form)
        if (user_exits(form['username'])):
            flash("Username '"+form['username']+"' is taken")
            return redirect('SignUpTrainer')
        
        else:
            # Changing goals from csv to array
            goals = form['goals'].split(",")
            # Removing empty elemets and sorting it alphabetically
            goals = sorted([i for i in goals if i])

            print(goals)
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
#@login_required
def Home():
    recent_rooms = get_rooms_by_trainee_id(current_user.username,2)
    return render_template('home.html',recent_rooms=recent_rooms)

@app.route('/TrainerSearch')
#@login_required
def TrainerSearch():
    return render_template('trainer-search.html', trainers = get_trainers())

@app.route('/logout')
#@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/chat/<uname>')
@login_required
def sessions(uname):
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

    return render_template('session.html',uname = uname, curr_uname = current_user.username,
                            curr_fname = current_user.fname, curr_lname = current_user.lname, 
                            rooms=ROOMS, messages = messages, curr_room = curr_room)
                    

@socketio.on('message')
def message(data):
    print(data['room_id'])
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

@socketio.on('join')
def join(data):
    print(data['room_name'])
    join_room(data['room'])
    send({'msg':data['uname'] + " has joined the " + data['room_name'] + " room."},
          room=data['room']
         )

@socketio.on('leave')
def leave(data):

    leave_room(data['room_name'])
    send({'msg': data['uname'] +" has left the " + data['room_name'] + " room."},
          room=data['room']
         )