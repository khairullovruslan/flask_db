from os import abort

from flask import Flask, url_for, request, render_template, make_response, jsonify
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.departments import Department
from data.jobs import Jobs
from data.users import User
from forms.DepartmentsForm import DepartmentForm
from forms.JobsForm import JobsForm
from forms.loginform import LoginForm
from forms.user import RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        departments1 = db_sess.query(Department).all()

    return render_template("departaments.html", departments=departments1)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        jobs = db_sess.query(Jobs).filter(
            (Jobs.user == current_user) | (Jobs.is_finished != True))
    else:
        jobs = db_sess.query(Jobs).filter(Jobs.is_finished != True)

    return render_template("index.html", jobs=jobs)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


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
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/success")
def success():
    return render_template('success.html')


@app.route("/table/<gender>/<int:age>")
def table(gender, age):
    params = {'title': 'Цвет каюты',
              'gender': gender,
              'age': age}
    return render_template('table.html', **params)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.title.data
        jobs.team_leader_id = form.team_leader_id.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление работы',
                           form=form)


@app.route('/department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department()
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data
        current_user.department.append(department)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/departments')
    return render_template('department.html', title='Add Department',
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter((Jobs.id == id) | (Jobs.id == 1),
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            form.title.data = jobs.job
            form.team_leader_id.data = jobs.team_leader_id
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter((Jobs.id == id) | (Jobs.id == 1),
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            jobs.job = form.title.data
            jobs.team_leader_id = form.team_leader_id.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        departments = db_sess.query(Department).filter((Department.id == id) | (Department.id == 1),
                                                       Department.user == current_user).first()
        if departments:
            form.title.data = departments.title
            form.chief.data = departments.chief
            form.members.data = departments.members
            form.email.data = departments.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        departments = db_sess.query(Department).filter((Department.id == id) | (Department.id == 1),
                                                       Department.user == current_user).first()
        if departments:
            departments.title = form.title.data
            departments.chief = form.chief.data
            departments.members = form.members.data
            departments.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('department.html',
                           title='Edit Department',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter((Jobs.id == id) | (Jobs.id == 1),
                                      Jobs.user == current_user
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).filter((Department.id == id) | (Department.id == 1),
                                                   Department.user == current_user
                                                   ).first()
    if departments:
        db_sess.delete(departments)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


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


# def user_get():
#     db_sess = db_session.create_session()
#     jobs = db_sess.query(Jobs).all()
#     for job in jobs:
#         print(job.team_leader.surname, job.team_leader.name, job.work_size, job.is_finished)


def jobs_add():
    db_sess = db_session.create_session()
    job = Jobs()
    job.team_leader_id = 1
    job.job = 'aadadada;dhakdakdgakdbak'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = True
    db_sess.add(job)
    db_sess.commit()


def departments_add():
    db_sess = db_session.create_session()
    department = Department()
    department.title = 'Department of geological exploration'
    department.chief = 1
    department.members = '3, 4, 5'
    department.email = 'geo@mars.org'
    db_sess.add(department)
    db_sess.commit()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    # departments_add()
    # user_add()
    # jobs_add()
    app.run(port=8080, host='127.0.0.1')
