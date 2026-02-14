
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    question = db.Column(db.String(500))
    option1 = db.Column(db.String(200))
    option2 = db.Column(db.String(200))
    option3 = db.Column(db.String(200))
    option4 = db.Column(db.String(200))
    answer = db.Column(db.String(200))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(username=request.form['username'],
                    password=request.form['password'],
                    role=request.form['role'])
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'],
                                    password=request.form['password']).first()
        if user:
            session['user'] = user.username
            session['role'] = user.role
            return redirect('/dashboard')
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    exams = Exam.query.all()
    return render_template("dashboard.html", exams=exams)

@app.route('/create_exam', methods=['GET', 'POST'])
def create_exam():
    if request.method == 'POST':
        exam = Exam(title=request.form['title'],
                    question=request.form['question'],
                    option1=request.form['option1'],
                    option2=request.form['option2'],
                    option3=request.form['option3'],
                    option4=request.form['option4'],
                    answer=request.form['answer'])
        db.session.add(exam)
        db.session.commit()
        return redirect('/dashboard')
    return render_template("create_exam.html")

@app.route('/take_exam/<int:id>', methods=['GET', 'POST'])
def take_exam(id):
    exam = Exam.query.get(id)
    if request.method == 'POST':
        selected = request.form['option']
        score = 1 if selected == exam.answer else 0
        return render_template("result.html", score=score)
    return render_template("take_exam.html", exam=exam)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
