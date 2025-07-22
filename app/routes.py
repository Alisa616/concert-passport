from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from sqlalchemy.testing.pickleable import User

from . import db
from .models import Concerts, Users
from datetime import datetime


login_manager = LoginManager()


def init_routes(app):

    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.filter_by(email=user_id).first()

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route("/concerts")
    def show_concerts():
        concerts = Concerts.query.order_by(Concerts.event_date).all()

        return render_template('concerts.html', concerts=concerts)

    @app.route("/concerts/<int:concert_id>")
    def concert_detail(concert_id):
        concert = Concerts.query.get_or_404(concert_id)
        return render_template('concert_detail.html', concert=concert)

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            city = request.form.get('city') or None
            birthday_str = request.form.get('birthday')
            birthdate = datetime.strptime(birthday_str, '%Y-%m-%d') if birthday_str else None
            password = request.form['password']
            print(f"Вот пароль {password}")

            if Users.query.filter_by(email=email).first():
                flash('Пользователь с таким email уже существует')
                return redirect(url_for('register'))

            new_user = Users(
                name=name,
                email=email,
                city=city,
                birth_date=birthdate
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            return redirect(url_for('login'))

        return render_template('register.html')


    @app.route("/login", methods=['GET', 'POST'])
    @login_required
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = Users.authenticate(email, password)

            if user:
                login_user(user)
                return redirect(url_for('show_concerts'))
            else:
                flash('Неверный логин или пароль', 'danger')

        else:
            flash('Форма заполнена некорректно', 'danger')

        return render_template('login.html')

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash('Вы вышли из системы', 'success')
        return redirect(url_for('show_concerts'))










