# run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("🎵 Запуск сайта концертов 🎵")
    print("=" * 50)
    print("Для первого запуска выполните:")
    print("python init_db.py")
    print("=" * 50)

    app.run(debug=True, host='127.0.0.1', port=5000)