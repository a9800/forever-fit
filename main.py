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
        # Boolean to check if username is taken
        created = create_user(form_data, "True")
        return redirect('/')
        
@app.route('/SignUpTrainer',methods = ['POST', 'GET'])
def SignUpTrainer():
    if request.method == 'GET':
        return render_template('signup-trainer.html')

    if request.method == 'POST':
        form_data = request.form
        print(form_data)
        # Boolean to check if username is taken
        created = create_user(form_data, "True")
        return redirect('/')
        
def create_user(form_data, is_trainer):
    conn = sqlite3.connect('forever-fit.db')

    user = conn.execute("SELECT COUNT(*) AS NUMUSERS FROM USERS WHERE \
                         UNAME = '"+form_data["username"]+"';")
    
    for row in user:
        num_users = (row[0])
    
    if (num_users > 0):
        conn.commit()
        return False
    else:
        conn.execute("INSERT INTO users (UNAME,FNAME,LNAME,DOB,PASSWORD,ISTRAINER,FITNESS_GOALS) \
                      VALUES (\
                      '"+form_data["username"]+"',\
                      '"+form_data["fname"]+"',\
                      '"+form_data["lname"]+"',\
                      '"+form_data["birthday"]+"',\
                      '"+form_data["psw"]+"',\
                      "+is_trainer+",\
                      '"+form_data["goals"]+"')");

        user = conn.execute("SELECT COUNT(*) AS NUMUSERS FROM USERS")
        for row in user:
            print(row[0])
    
        conn.commit()
        return True


if __name__ == "__main__":
    app.run()