

### Описание проекта:
Проект представляет собой API для сервиса публикации рецептов приготовления блюд
### Технологии:
- Python 3.7
- Django 3.2
- DRF
- Docker
- Postgresql
- Nginx
- Gunicorn

### Как запустить проект:
#### 1. Клонируте репозиторий `$ git clone git@github.com:nikinika/foodgram-project-react.git`
#### 2. В директории `infra/`, командой `$touch .env`, создайте файл `.env` со следующими переменными
- DJANGO_KEY='ваш secret_key django'
- DB_ENGINE=django.db.backends.postgresql
- DB_NAME= название БД
- POSTGRES_USER= ваше имя пользователя
- POSTGRES_PASSWORD= пароль для доступа к БД
- DB_HOST=db
- DB_PORT=5432
- SECRET_KEY=<Тут должен быть секретный ключ из settings.py, но я не буду его писать>
- DEBUG=False
- ALLOWED_HOSTS=*
#### 3. В терминале находясь в папке `infra/` выполните комманду
#### `$ docker-compose up -d` или `$ docker-compose up -d --build`
#### если нужно пересобрать контейнеры
#### 4. Создайте файлы миграции `$ docker-compose exec backend python manage.py makemigrations`
#### 5. Примените миграции `$ docker-compose exec backend python manage.py migrate`
#### 6. Соберите статику `$ docker-compose exec backend python manage.py collectstatic --no-input`
#### 7. Для доступа к админке создайте суперюзера `$ docker-compose exec backend python manage.py createsuperuser`
#### 8. Чтобы загрузить в базу данные об ингредиентах `$ docker-compose exec backend python manage.py load_ing`


### Документация по эндпоинтам, запросам и ответам:

 http://localhost/api/docs/

### Проект размещен по адресу

http://51.250.21.175

### Реквизиты суперюзера

- login: admin
- e-mail: admin@admin.ru
- password: admin

### Разработчик:
Никитенко Николай 
