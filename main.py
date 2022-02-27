from flask import Flask

from data import db_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def user_add():
    db_sess = db_session.create_session()
    user = User()
    user.surname = 'Scott'
    user.name = 'Ridley'
    user.age = 21
    user.position = 'captain'
    user.speciality = 'research engineer'
    user.address = 'module_1'
    user.email = 'scott_chief@mars.org'

    db_sess.add(user)
    user = User()
    user.surname = 'Иван'
    user.name = 'Петров'
    user.age = 20
    user.position = 'Рядовой'
    user.speciality = 'engineer'
    user.address = 'module_2'
    user.email = 'ivan@mars.org'

    db_sess.add(user)
    user = User()
    user.surname = 'Дима'
    user.name = 'Петров'
    user.age = 16
    user.position = 'captain'
    user.speciality = 'engineer'
    user.address = 'module_1'
    user.email = 'petrov@mars.org'

    db_sess.add(user)

    db_sess.commit()

def jobs_add():
    db_sess = db_session.create_session()
    job = Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False
    db_sess.add(job)
    db_sess.commit()


def user_get():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == 1).first()
    for news in user.news:
        print(news.created_date)


def news_add():
    pass


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    user_add()
    news_add()
    jobs_add()
#  app.run(port=8080, host='127.0.0.1')
