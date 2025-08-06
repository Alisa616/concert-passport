from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from . import db
from .models import Concerts, Users


def init_routes(app):
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
            password = request.form['password']

            # Проверяем дату рождения
            birthdate = None
            if birthday_str:
                birthdate = datetime.strptime(birthday_str, '%Y-%m-%d').date()

            # Проверяем, существует ли пользователь
            if Users.query.filter_by(email=email).first():
                flash('Пользователь с таким email уже существует', 'danger')
                return redirect(url_for('register'))

            # Создаем нового пользователя
            new_user = Users(
                name=name,
                email=email,
                city=city,
                birth_date=birthdate
            )
            new_user.set_password(password)

            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при регистрации. Попробуйте еще раз.', 'danger')
                return redirect(url_for('register'))

        return render_template('register.html')

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            user = Users.authenticate(email, password)
            if user:
                login_user(user)
                flash(f'Добро пожаловать, {user.name}!', 'success')
                return redirect(url_for('show_concerts'))
            else:
                flash('Неверный логин или пароль', 'danger')

        return render_template('login.html')

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash('Вы вышли из системы', 'success')
        return redirect(url_for('index'))