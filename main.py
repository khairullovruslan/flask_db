from flask import Flask

from data import db_session
from data.users import User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def user_add():
    user = User()
    user.name = "Пользователь 1"
    user.about = "биография пользователя 1"
    user.email = "email@email.ru"
    user.set_password("123456")

    user2 = User(name="Пользователь 2",
                 about="биография пользователя 2",
                 email="email2@email.ru")
    user2.set_password("1234")

    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.add(user2)
    db_sess.commit()


def user_get():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == 1).first()
    for news in user.news:
        print(news.created_date)


def news_add():
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

    db_sess.commit()


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    # user_add()
    news_add()
#  app.run(port=8080, host='127.0.0.1')
