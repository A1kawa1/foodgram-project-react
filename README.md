# praktikum_new_diplom

Это проект для публикации собственных рецептов, просмотра чужих, подписок на авторов и многое другое.  
В нем реализованны связь бэкенда на django и фронтенда на js через docker-compose.  
проект - 158.160.53.112  
почта админки - test@mail.ru  
пароль админки - testadmintest

### Стек технологий:

- Python
- Django
- Django Rest Framework
- PostreSQL
- Nginx
- Docker

### Как запустить проект:

Склонировать репозиторий себе локально  
```
git clone https://github.com/A1kawa1/foodgram-project-react.git
```

```
В директории foodgram-project-react/infra создать файл .env
```

Заполнить .env  
```
DB_ENGINE=django.db.backends.postgresql  
DB_NAME=postgres  
POSTGRES_USER=postgres  
POSTGRES_PASSWORD=postgres  
DB_HOST=db  
DB_PORT=5432  
```

Собрать необходимые контейнеры  
```
docker-compose up -d --build
```

Выполняем миграции  
```
docker-compose exec web python manage.py migrate
```

Создаем суперпользователя  
```
docker-compose exec web python manage.py createsuperuser
```

Cобираем статику  
```
docker-compose exec web python manage.py collectstatic --no-input
```

### Документация API YaMDb:

Документация доступна по эндпойнту: http://localhost/api/docs/