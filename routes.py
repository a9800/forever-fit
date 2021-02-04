from flask import Flask, flash, request, render_template, redirect
from flask_login import current_user, login_user, LoginManager, login_required, UserMixin
from form import *
from sql_db import *
from main import app, login



@app.route("/")
def home():
    return render_template('index.html')

@app.route('/SignUp')
def SignUp():
    return render_template('signup.html')

@app.route('/SignUpTrainee',methods = ['POST', 'GET'])
def SignUpTrainee():
    if request.method == 'GET':
        return render_template('signup-trainee.html')

    if request.method == 'POST':
        form = request.form
        print(form)
        if (user_exits(form['username'])):
            return redirect('SignUpTrainee')
        
        else:
            register = User(username = form['username'], fname = form['fname'],
                            lname = form['lname'], dob = form['birthday'], isTrainer = False,
                            fitnessGoals = form['goals'])
                            
            register.set_password(form['psw'])
            db.session.add(register)
            db.session.commit()
            return redirect('Login')
        
@app.route('/SignUpTrainer',methods = ['POST', 'GET'])
def SignUpTrainer():
    if request.method == 'GET':
        return render_template('signup-trainer.html',form=RegisterForm())

    if request.method == 'POST':
        form = request.form
        print(form)
        if (user_exits(form['username'])):
            return redirect('SignUpTrainer')
        
        else:
            register = User(username = form['username'], fname = form['fname'],
                            lname = form['lname'], dob = form['birthday'], isTrainer = True,
                            fitnessGoals = form['goals'])

            register.set_password(form['psw'])
            db.session.add(register)
            db.session.commit()
            return redirect('Login')

@app.route('/Test')
@login_required
def Test():
    return "Test"

@app.route('/Login',methods = ['POST','GET'])
def Login():
    if current_user.is_authenticated:
        return redirect('Test')
     
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username = username).first()
        
        if user is not None and user.check_password(request.form['psw']):
            print(user is not None and user.check_password(request.form['psw']))
            login_user(user)
            return redirect('Test')
     
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
