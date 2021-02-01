from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

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
        form_data = request.form
        print(form_data)
        return redirect('/')
        
@app.route('/SignUpTrainer',methods = ['POST', 'GET'])
def SignUpTrainer():
    if request.method == 'GET':
        return render_template('signup-trainer.html')

    if request.method == 'POST':
        form_data = request.form
        print(form_data)
        return redirect('/')
        


if __name__ == "__main__":
    app.run()