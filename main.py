from flask import Flask, url_for, request, render_template
from werkzeug.utils import redirect

from data import db_session
from data.news import News
from data.users import User
from forms.loginform import LoginForm
from forms.user import RegisterForm

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

    news = News(title="Первая новость", content="Привет блог!",
                user_id=1, is_private=False)
    user = db_sess.query(User).filter(User.email == "email@email.ru").first()
    news2 = News(title="Вторая новость", content="Уже вторая запись!",
                 user=user, is_private=False)

    news3 = News(title="Вторая новость", content="Уже вторая запись!",
                 user_id=2, is_private=False)

    db_sess.add(news)
    db_sess.add(news2)
    db_sess.add(news3)
    db_sess.commit()


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    # user_add()
    user_get()
    # news_add()
    app.run(port=8080, host='127.0.0.1')
