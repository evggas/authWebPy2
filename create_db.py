from app import db, app  # Импортируем приложение и базу данных
from app.models import User  # Импортируем модели

# Создаём таблицы
with app.app_context():
    db.create_all()
    print("База данных и таблицы успешно созданы.")
