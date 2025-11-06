import os

from flask import render_template, request, url_for, flash, redirect, current_app
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, date

from werkzeug.utils import secure_filename

from . import db
from .models import Concerts, Users


def init_routes(app):
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    def save_profile_photo(file, user_id):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            filename = f'user_{user_id}_{name}{ext}'

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            return filename

        return None

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
            name = (request.form.get('name') or "").strip()
            raw_email = (request.form.get('email') or "").strip()
            email = raw_email.lower()
            city = (request.form.get('city') or "").strip() or None
            password = (request.form.get('password') or "")
            birthday_str = (request.form.get('birthday') or "").strip()

            errors = ""
            if not name:
                errors +="Введите имя."
            if not email:
                errors += "Введите email."
            if not password or len(password) < 6:
                errors += "Пароль должен быть не короче 6 символов."
            if errors:
                flash(errors.strip(), "danger")
                return redirect(url_for('register'))

            # Проверяем дату рождения
            birthdate = None
            if birthday_str:
                try:
                    birthdate = date.fromisoformat(birthday_str)
                except ValueError:
                    flash('Некорректная дата', 'danger')
                    return redirect(url_for('register'))

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
                current_app.logger.exception("Ошибка регистрации")
                flash(f'Ошибка при регистрации: {type(e).__name__}', 'danger')
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

    @app.route("/profile", methods=['GET', 'POST'])
    @login_required
    def profile():
        if request.method == 'POST':
            # Обновляем данные пользователя
            current_user.name = request.form['name']
            current_user.city = request.form.get('city') or None

            birthday_str = request.form.get('birthday')
            if birthday_str:
                current_user.birth_date = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            else:
                current_user.birth_date = None

            if 'profile_photo' in request.files:
                file = request.files['profile_photo']

                if file.filename != '':
                    if current_user.profile_photo:
                        old_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.profile_photo)
                        if os.path.exists(old_photo_path):
                            try:
                                os.remove(old_photo_path)
                            except:
                                pass

                    filename = save_profile_photo(file, current_user.id)
                    if filename:
                        current_user.profile_photo = filename
                        flash('Фото профиля обновлено', 'success')
                    else:
                        flash('Ошибка загрузки фото', 'danger')


            new_password = request.form['new_password']
            if new_password:
                current_user.set_password(new_password)

            try:
                db.session.commit()
                flash("Профиль успешно обновлен", "success")
            except Exception as e:
                db.session.rollback()
                flash("Ошибка при обновлении профиля", "danger")
            return redirect(url_for('profile'))

        concerts_attended = len(current_user.attendance)
        return render_template("profile.html",
                               user=current_user,
                               concerts_attended=concerts_attended)

    @app.route("/delete_photo", methods=['POST'])
    @login_required
    def delete_photo():
        if current_user.profile_photo:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.profile_photo)
            if os.path.exists(photo_path):
                try:
                    os.remove(photo_path)
                except:
                    pass

            current_user.profile_photo = None
            try:
                db.session.commit()
                flash('Фото профиля удалено', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при удалении фото', 'danger')

        return redirect(url_for('profile'))

    @app.route("/admin/add_artist", methods=['GET', 'POST'])
    @login_required
    def add_artist():
        """Добавление нового артиста (только для админа)"""
        if not current_user.is_admin:
            flash("Доступ запрещен. Доступ только для администраторов", "danger")
            return redirect(url_for('profile'))

        if request.method == 'POST':
            name = request.form['name']
            genre = request.form.get('genre') or None

            from .models import Artists
            existing_artist = Artists.query.filter_by(name=name).first()
            if existing_artist:
                flash(f"Артист {name} уже существует", "warning")
                return redirect(url_for('add_artist'))

            new_artist = Artists(name=name, genre=genre)

            try:
                db.session.add(new_artist)
                db.session.commit()
                flash(f"Артист {name} успешно добавлен", "success")
                return redirect(url_for('add_concert'))
            except Exception as e:
                db.session.rollback()
                flash("Ошибка при добавлении арстиста", "danger")
        return render_template("admin/add_artist.html")

    @app.route("/admin/add_concert", methods=['GET', 'POST'])
    @login_required
    def add_concert():
        """Добавление нового концерта (только для админа)"""
        if not current_user.is_admin:
            flash("Доступ запрещен. Доступ только для администраторов", "danger")
            return redirect(url_for('profile'))

        from .models import Artists
        artists = Artists.query.all()

        if request.method == 'POST':
            artist_id = request.form['artist_id']
            city = request.form['city']
            event_date_str = request.form['event_date']
            venue = request.form.get('venue') or None
            event_type = request.form['event_type']

            try:
                event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash("Неправильный формат даты", "danger")
                return redirect(url_for('add_concert'))

            new_concert = Concerts(
                artist_id=int(artist_id),
                city=city,
                event_date=event_date,
                venue=venue,
                event_type=event_type
            )

            try:
                db.session.add(new_concert)
                db.session.commit()
                artist = Artists.query.get(artist_id)
                flash(f"Концерт {artist.name} в {city} успешно добавлен", "success")
                return redirect(url_for('add_concert'))
            except Exception as e:
                db.session.rollback()
                flash("Ошибка при добавлении концерта", "danger")

        return render_template("admin/add_concert.html", artists=artists)

    @app.route("/admin/manage_concerts")
    @login_required
    def manage_concerts():
        """Управление концертами (только для админа)"""
        if not current_user.is_admin:
            flash("Доступ запрещен. Только для админов", "danger")
            return redirect(url_for('profile'))

        concerts = Concerts.query.order_by(Concerts.event_date.desc()).all()
        return render_template("admin/manage_concerts.html", concerts=concerts)

    @app.route("/admin/delete_concert/<int:concert_id>", methods=['POST'])
    @login_required
    def delete_concert(concert_id):
        """Удаление концертов (только для админа)"""
        if not current_user.is_admin:
            flash("Доступ запрещен. Доступ только для администраторов", "danger")
            return redirect(url_for('profile'))

        concert = Concerts.query.get_or_404(concert_id)
        artist_name = concert.artist.name
        city = concert.city

        try:
            db.session.delete(concert)
            db.session.commit()
            flash(f"Концерт {artist_name} в {city} удален", "success")
        except Exception as e:
            db.session.rollback()
            flash("Ошибка при удалении концерта", "danger")

        return redirect(url_for("manage_concerts"))


