from flask import Flask, url_for, request, render_template
from werkzeug.utils import redirect

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.loginform import LoginForm
from forms.user import RegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            address=form.address.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.username.data).first()
        if user and user.check_password(form.password.data):
            return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/success")
def success():
    return render_template('success.html')


def user_add():
    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"

    user2 = User(surname="Brown",
                 name="Mark",
                 age="24",
                 position="helmsman1",
                 speciality="engineer",
                 address="module_2",
                 email="brown_helmsman@email.ru")

    user3 = User(surname="Malone",
                 name="Jack",
                 age="25",
                 position="helmsman2",
                 speciality="engineer",
                 address="module_3",
                 email="malone_helmsman@email.ru")

    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.add(user2)
    db_sess.add(user3)
    db_sess.commit()


def user_get():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    for job in jobs:
        print(job.team_leader.surname, job.team_leader.name, job.work_size, job.is_finished)


def jobs_add():
    db_sess = db_session.create_session()
    job = Jobs()
    job.team_leader_id = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False
    db_sess.add(job)
    db_sess.commit()


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    # user_add()
    # user_get()
    # jobs_add()
    app.run(port=8081, host='127.0.0.1')
