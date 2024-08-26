# Проект «Фудграм»
«Фудграм» — сайт, на котором пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Зарегистрированным пользователям доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Проект развернут на удаленном сервере по адресу `https://foodgram-alina.zapto.org`.

## Технологии
Python, Django, Django REST Framework, PostgreSQL, Gunicorn, Nginx, Docker, Docker Volumes, Docker Compose, Docker Hub, GitHub Actions.

## Как запустить проект локально
В терминале выполните команду по клонированию репозитория:
```
git clone https://github.com/alina-afsatarova/foodgram.git
```
Перейдите в склонированный репозиторий:
```
cd foodgram
```
Cоздайте и активируйте виртуальное окружение:
```
python -m venv env
```
```
source venv/Scripts/activate
```
Установите зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
cd backend
```
```
pip install -r requirements.txt
```
Перейдите в директорию infra:
```
cd ../infra
```
Создайте файл .env и заполните его в соответствии с файлом .env.example
```
touch .env
```
Запустите контейнеры локально:
```
docker compose up
```
После запуска откройте второй терминал и выполните следующие команды:

 - Сбор статики Django:
```
docker compose exec backend python manage.py collectstatic
```
 - Копирование статики в папку /backend_static/static/:
```
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
```
 - Применение миграций:
```
docker compose exec backend python manage.py migrate
```
 - Заполнения базы данных тестовыми данными:
```
docker compose exec backend python manage.py upload_tags
```
```
docker compose exec backend python manage.py upload_ingredients
```
 - Создание суперпользователя:
```
docker compose exec backend python manage.py createsuperuser
```

После запуска проекта главная страница доступна по адресу `http://127.0.0.1:8080/`.

Документация API доступна по адресу `http://127.0.0.1:8080/api/docs/`.

Админ-зона django доступна по адресу `http://127.0.0.1:8080/admin/`.


# Автор:
[Алина Афсатарова](https://github.com/alina-afsatarova/)

Telegram @alina_afsatarova
