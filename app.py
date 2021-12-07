from flask import Flask, render_template, request, redirect, session, url_for
from flask_avatar import Avatar
from functools import wraps
from exts import db
from models import User, Question, Comment
import os
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
Avatar(app)


@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by(Question.create_time).all()
    }
    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter_by(telephone=telephone, password=hashlib.md5(password.encode('utf-8')).hexdigest()).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            context = {
                'wrong': 'Wrong account or password, please try again!'
            }
            return render_template('login.html', **context)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # check telephone number
        user = User.query.filter_by(telephone=telephone).first()
        if telephone.isdigit() is False or len(telephone) != 11 or username is None or password is None\
                or password2 != password:
            return redirect(url_for('register'))
        if user:
            context = {
                'register_wrong': 'The phone number has been registered!'
            }
            return render_template('register.html', **context)
        else:
            user = User(telephone=telephone, username=username, password=hashlib.md5(password.encode('utf-8')).hexdigest())
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/new_question', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        new_question = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        new_question.author = user
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>', methods=['GET', 'POST'])
def detail(question_id):
    question = Question.query.filter_by(id=question_id).first()
    return render_template('detail.html', question=question)


@app.route('/comment/<question_id>', methods=['POST'])
def comment(question_id):
    content = request.form.get('comment_content')
    comment = Comment(content=content)
    question = Question.query.filter_by(id=question_id).first()
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    comment.author = user
    comment.question = question
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run(debug=True)
