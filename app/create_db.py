from app import create_app
from app.models import db, Users, Artists, Concerts, Attendance

app = create_app()
def create_db():
    with app.app_context():
        try:
            print('Начало')
            #from . import models
            #db.create_all()
            artist = Artists(
                name='Melanie Martinez',
                genre='pop'
            )
            db.session.add(artist)
            db.session.commit()

            print(Artists.query.all())
            print('Артист добавлен')

        except Exception as e:
            db.session.rollback()
            print('Ошибка при сохранении')

if __name__ == '__main__':
    create_db()
