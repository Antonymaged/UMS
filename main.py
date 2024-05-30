from sqlalchemy.orm import sessionmaker
from time import sleep
from flask import Flask,render_template, request, abort, redirect
# from flask_wtf import wtforms
# from wtforms import StringField, PasswordField, SubmitField
import log,mn
import subprocess

app = Flask(__name__)
Session = sessionmaker()(bind=log.engine)
session = sessionmaker()(bind=mn)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/la", methods=['POST','GET'])
def la():

    name = request.form['un']
    passw = request.form['pass']
    user = Session.query(log.University).filter(log.University.name == name).first()
    if user:
        if user.passw == passw:
            return redirect("/main")
    else:
        sleep(3)
        return redirect("/login")
    error_message = "Password is wrong"
    sleep(2)
    return render_template('login.html', error_message=error_message)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/reg", methods=['POST','GET'])
def reg():
    name = request.form['user']
    pass1 = request.form['pass1']
    pass2 = request.form['pass2']
    emai = request.form['em']
    if pass1 != pass2:
        error_message = "Password is wrong"
        sleep(2)
        return render_template('register.html', error_message=error_message)
    mn.m(name)
    data = log.University(nam=name, passw=pass1,email=emai)
    Session.add(data)
    Session.commit()
    return redirect("/main")

@app.route("/main")
def m():
    return render_template("main.html")


Session.close()
session.close()
app.run(debug=True,port=5500)