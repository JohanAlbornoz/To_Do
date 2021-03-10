import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask import Flask, render_template
from flask_app import model
import datetime
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, SelectField, PasswordField, validators
from wtforms.fields.html5 import DateField, TimeField, IntegerField, EmailField
from flask import Flask, render_template, redirect, request, url_for
from flask_session import Session

development_env = os.environ.get('FLASK_ENV') == 'development'

app = Flask(__name__)

app.config['WTF_CSRF_ENABLED'] = True
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
CSRFProtect(app)

if not development_env:
    from flask_talisman import Talisman
    Talisman(app, content_security_policy={
        'default-src' : '\'none\'',
        'style-src': [ 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css', '\'self\'' ],
        'img-src' : ['\'self\''],
        'script-src' : [ 'https://kit.fontawesome.com/0dac341963.js']
    })

@app.route('/')
def sign_up():
    return redirect('login')
    

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.DataRequired()])



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            connection = model.connect()
            user = model.get_user(connection, form.email.data, form.password.data)
            session['user'] = user 
            return redirect(url_for('home'))
        except Exception as exception:
            app.log_exception(exception)
    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    if 'user' not in session:
        return redirect(url_for('login'))
    session.pop('user')
    return redirect(url_for('home'))


@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    connection = model.connect()
    user_id = session['user']['id']
    limitated_tasks_user = model.limitated_tasks_user(connection, user_id)
    return render_template('home.html', limitated_tasks_user=limitated_tasks_user)

class TasksForm(FlaskForm):
    title = StringField('title', validators=[validators.DataRequired(), validators.length(min=3, max=40)])
    description = StringField('description', validators=[ validators.length(min=0, max=400)])
    due_date = DateField('due_date', validators=[validators.DataRequired()])


@app.route('/liste', methods=['GET', 'POST'])
def create_task():
    if 'user' not in session:
        return redirect(url_for('login'))
    connection = model.connect()
    user_id = session['user']['id']
    tasks_user = model.tasks_user(connection, user_id)
    try:
        task_do = int(request.cookies['task_do'])
    except:
        task_do = None
    list_task = model.tasks(connection)
    form = TasksForm(request.form)
    if form.validate_on_submit():
        try:
            connection = model.connect()
            date = datetime.datetime.now()
            task = { 
                'id': None, 
                'title': form.title.data,
                'description' : form.description.data, 
                'creation_date' : date,
                'due_date' : form.due_date.data,
                'id_user' : user_id
            }
            model.insert_task(connection, task)
            return redirect('/liste')
        except Exception as exception:
            app.log_exception(exception)
    return render_template('liste.html', form=form, liste=list_task, tasks_user=tasks_user, task_do=task_do)


@app.route('/liste/delete/<int:task_id>', methods=['POST'])
def task_delete(task_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    connection = model.connect()
    model.delete_task(connection, task_id)
    return redirect(url_for('create_task'))

@app.route('/liste/do/<int:task_id>', methods=['POST'])
def task_do(task_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    response = redirect(url_for('create_task'))
    response.set_cookie('task_do', str(task_id))
    return response

