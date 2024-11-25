from flask import render_template, request, redirect, url_for, flash  # Для работы с шаблонами и уведомлениями
from flask_login import login_user, logout_user, current_user, login_required  # Для работы с пользователями
from app import app, db, bcrypt  # Приложение, база данных и хеширование паролей
from app.forms import RegistrationForm, LoginForm, UpdateProfileForm  # Формы из файла forms.py
from app.models import User  # Модель пользователя

# Главная страница
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)

# Вход в систему
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Вы вошли в систему!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Неправильный email или пароль.', 'danger')
    return render_template('login.html', title='Вход', form=form)

# Выход из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('home'))

# Страница аккаунта (общая информация)
@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Аккаунт')

# Редактирование профиля
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()

    # Если форма валидна, обновляем данные
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        # Если введён новый пароль, обновляем его
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password

        # Сохраняем изменения в базе
        db.session.commit()

        # Добавляем сообщение об успешном обновлении
        flash('Ваш профиль был успешно обновлён!', 'success')

        # Перенаправляем пользователя обратно на страницу профиля
        return redirect(url_for('profile'))

    # Если запрос GET, предзаполняем форму текущими данными
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('profile.html', title='Редактировать профиль', form=form)
