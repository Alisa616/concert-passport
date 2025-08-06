from app import create_app, db
from app.models import Users, Artists, Concerts, Attendance
from datetime import date


def init_database():
    """Создает таблицы и добавляет начальные данные"""
    app = create_app()

    with app.app_context():
        try:
            print('Создание таблиц...')
            db.create_all()

            # Проверяем, есть ли уже данные
            if Artists.query.first():
                print('Данные уже существуют!')
                return

            print('Добавление артистов...')
            artists = [
                Artists(name='Luna Serenade', genre='Indie Folk'),
                Artists(name='Kairo Blaze', genre='Electronic Dance'),
                Artists(name='Elena Volkov', genre='Classical Crossover'),
                Artists(name='Jaxon Ryder', genre='Hip-Hop/Rap')
            ]
            db.session.add_all(artists)
            db.session.commit()

            print('Добавление концертов...')
            concerts = [
                Concerts(
                    artist_id=1,
                    city='New York',
                    event_date=date(2025, 10, 19),
                    venue='Madison Square Garden',
                    event_type='solo'
                ),
                Concerts(
                    artist_id=2,
                    city='Seattle',
                    event_date=date(2025, 11, 20),
                    venue='The Crocodile',
                    event_type='solo'
                ),
                Concerts(
                    artist_id=3,
                    city='Нижний Новгород',
                    event_date=date(2025, 12, 3),
                    venue='Premio Concert Hall',
                    event_type='solo'
                ),
                Concerts(
                    artist_id=4,
                    city='Washington',
                    event_date=date(2025, 10, 11),
                    venue='9:30 Club',
                    event_type='solo'
                )
            ]
            db.session.add_all(concerts)
            db.session.commit()

            print('База данных успешно инициализирована!')

        except Exception as e:
            db.session.rollback()
            print(f'Ошибка при инициализации БД: {e}')


if __name__ == '__main__':
    init_database()