import os
from app import create_app, db

def update_database():
    app = create_app()

    with app.app_context():
        try:
            print('Обновление структуры дб')
            basedir = os.path.abspath(os.path.dirname(__file__))
            upload_folder = os.path.join(basedir, 'app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            print(f'Папка создана: {upload_folder}')

            with db.engine.connect() as connection:
                result = connection.execute(db.text("""
                    SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'profile_photo'
                """))

                if not result.fetchone():
                    connection.execute(db.text("""
                    ALTER TABLE users
                    ADD COLUMN profile_photo VARCHAR(255) NOT NULL
                    """))

                    connection.commit()
                    print('Поле добавлено в таблицу')
                else:
                    print('Данное поле существует')

            print('База данных успешно обновлена')

        except Exception as e:
            print(f'Ошибка при обновлении бд: {e}')

if __name__ == '__main__':
    update_database()


