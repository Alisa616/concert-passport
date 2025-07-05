from . import create_app, db
from app.models import Users, Artists, Concerts, Attendance
from datetime import date

app = create_app()
with app.app_context():
    try:
        print('Начало')
        #from . import models
        #db.create_all()
        # artist = Artists(
        #     name='Melanie Martinez',
        #     genre='pop'
        # )
        # db.session.add(artist)
        # db.session.commit()

        print(Artists.query.all())
        print('Артист добавлен')
        artist_id = Artists.query.filter_by(name='Melanie Martinez').first()
        # db.session.add(artist)
        # db.session.commit()

        concert_1 = Concerts(
            artist_id=3,
            city='New York',
            event_date=date(2025,10,19),
            venue='club',
            event_type='solo'
        )

        concert_2 = Concerts(
            artist_id=4,
            city='Seattle',
            event_date=date(2050, 11, 20),
            venue='The crocodile',
            event_type='solo'
        )

        concert_3 = Concerts(
            artist_id=5,
            city='Нижний Новгород',
            event_date=date(2070, 1, 3),
            venue='Premio concert hall',
            event_type='solo'
        )

        concert_4 = Concerts(
            artist_id=6,
            city='Washington',
            event_date=date(2030, 10, 11),
            venue='9:30 club',
            event_type='solo'
        )
        # db.session.add(concert_1)
        # db.session.add(concert_2)
        # db.session.add(concert_3)
        # db.session.add(concert_4)
        # db.session.commit()

    except Exception as e:
        db.session.rollback()
        print('Ошибка при сохранении')