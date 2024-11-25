from app import db, app  # Импортируем приложение и базу данных
from app.models import User  # Импортируем модели

# Создаём таблицы
with app.app_context():  # Указываем, что работаем в контексте приложения
    db.create_all()  # Создаём все таблицы из моделей
    print("База данных и таблицы успешно созданы.")
