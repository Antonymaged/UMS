#!/usr/bin/python3
from time import sleep
from flask import Flask,render_template, request, redirect, session
from sqlalchemy import create_engine, Integer, Double, String, Column
from sqlalchemy.orm import declarative_base, sessionmaker
# from flask_wtf import wtforms
# from wtforms import StringField, PasswordField, SubmitField
import log

app = Flask(__name__)
app.config['SECRET_KEY'] = "I WANT TO DIE"

Session = sessionmaker()(bind=log.engine)
# sassion = sessionmaker()(bind=mn)
base = declarative_base()
class University(base):
    __tablename__ = "students"
    stu_id = Column(Integer, primary_key=True)
    stu_name = Column(String, nullable=False)
    stu_fac = Column(String, nullable=False)
    stu_lev = Column(Integer, nullable=False)
    stu_age = Column(Integer, nullable=False)
    stu_gpa = Column(Double, nullable=False)
    stu_numcor = Column(Integer, nullable=False)
    def __init__(self, nam, fac,lev,age,gpa,numcor):
        self.stu_name = nam
        self.stu_fac = fac
        self.stu_lev = lev
        self.stu_age = age
        self.stu_gpa = gpa
        self.stu_numcor = numcor

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
            session['var'] = name
            
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
    session['var'] = name
    data = log.University(nam=name, passw=pass1,email=emai)
    Session.add(data)
    Session.commit()
    return redirect("/main")

@app.route("/main")
def m():
    name = session.get('var')
    engine = create_engine('sqlite:///data/{}.db'.format(name), echo=False)


    base.metadata.create_all(engine)
    sassion = sessionmaker()(bind = engine)
    records = sassion.query(University).all()
    sassion.close()
    return render_template("main.html", records = records)

@app.route("/add", methods=['POST','GET'])
def add():
    return render_template("add.html")

@app.route("/ad", methods=['POST','GET'])
def ad():
    name = session.get('var')
    engine = create_engine('sqlite:///data/{}.db'.format(name), echo=False)
    sassion = sessionmaker()(bind = engine)
    rec = University(request.form['sn'],request.form['facn'],request.form['slev'],request.form['sage'],request.form['sgpa'],request.form['snoc'])
    sassion.add(rec)
    sassion.commit()
    redirect("/a")
    sassion.close()
    return redirect("/main")

@app.route("/edi", methods=['POST','GET'])
def edi():
    return render_template('edit.html')

@app.route("/ed", methods=['POST','GET'])
def ed():
    name = session.get('var')
    engine = create_engine('sqlite:///data/{}.db'.format(name), echo=False)
    sassion = sessionmaker()(bind = engine)
    id = sassion.query(University).filter_by(stu_id = request.form['sid']).first()
    if id:
        id.stu_name=request.form['sn']
        id.stu_fac=request.form['facn']
        id.stu_lev=request.form['slev']
        id.stu_age=request.form['sage']
        id.stu_gpa=request.form['sgpa']
        id.stu_numcor=request.form['snoc']
        sassion.commit()
    else:
        pass
    sassion.close()
    return redirect("/main")

@app.route("/del", methods=['POST','GET'])
def dele():
    return render_template("delete.html")

@app.route("/de", methods=['POST','GET'])
def de():
    name = session.get('var')
    engine = create_engine('sqlite:///data/{}.db'.format(name), echo=False)
    sassion = sessionmaker()(bind = engine)
    id = sassion.query(University).filter_by(stu_id = request.form['sid']).first()
    if id:
        sassion.delete(id)
        sassion.commit()
    else:
        pass
    sassion.close()
    return redirect("/main")

Session.close()
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
