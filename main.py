from flask import Flask, render_template, redirect
from register_form import RegisterForm
from login_form import LoginForm
from data import db_session
from data.users import User
from db_manager import get_users, check_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/users.db")
session = db_session.create_session()

USERNAME = ''

IS_LOGIN = False

MENU = [('cappuccino', 200), ('latte', 250), ('raf', 300), ('cocoa', 150), ('milk', 90), ('matcha', 135), ('tea', 80)]


@app.route('/')
def index():
    print(f'-------------------------{IS_LOGIN}-------------------------')
    return render_template("base.html")


@app.route("/menu")
def basket():
    return render_template("menu.html", menu=MENU)


@app.route("/basket")
def menu():
    return render_template("basket.html", username=USERNAME)


@app.route('/register', methods=['GET', 'POST'])
def register():
    global USERNAME
    global IS_LOGIN
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        if username not in get_users():
            surname = form.surname.data
            name = form.surname.data
            number = form.number.data
            email = form.email.data
            password = form.password.data
            is_remember = form.remember_me.data
            user = User()
            user.username = username
            user.surname = surname
            user.name = name
            user.number = number
            user.email = email
            user.password = password
            user.is_remember = is_remember
            session.add(user)
            session.commit()
            USERNAME = username
            IS_LOGIN = True
            return redirect('/login_menu')
        IS_LOGIN = False
        return redirect('/login_error')
    return render_template('register.html', title='Авторизация', form=form)


@app.route('/login_error')
def login_error():
    return render_template('login_error.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global USERNAME
    global IS_LOGIN
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        is_remember = form.remember_me.data
        USERNAME = username
        IS_LOGIN = True
        if check_user(username, password):
            return redirect('/login_menu')
        IS_LOGIN = False
        return 'Проверьте правильность введенных данных'
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/login_page')
def login_page():
    return render_template('login_page.html', username=USERNAME)


@app.route('/login_menu')
def login_menu():
    return render_template('login_menu.html', username=USERNAME, menu=MENU)


if __name__ == '__main__':
    app.run(debug=True)
