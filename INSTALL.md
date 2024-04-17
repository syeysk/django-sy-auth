## На Linux

Скачивание репозитория:

```sh
git clone https://github.com/syeysk/django-sy-auth
```

Заполнить переменные окружения, добавив и заполнив файл `.env`

Сборка образа:

```sh
docker-compose build
```

Развёртывание и запуск контейнера

```sh
docker-compose up -d
```

## На Windows

Скачивание репозитория:

```sh
git clone https://github.com/syeysk/django-sy-auth
```

Установка зависимостей:

```sh
pip install -r requirements.txt
```

Применение миграций:

```sh
python manage.py migrate
```

Сбор статических файлов:

```sh
python manage.py collectstatic
```


Заполнить переменные окружения, добавив и заполнив файл `.env`

Запуск сервера:

```sh
python manage.py runserver 8004
```

## Проверка доступности сервера

<http://127.0.0.1:8004/api/v1/schema/swagger-ui/>

## Если хотите, примените Nginx + Debian

Настройки для Nginx:

```
server {
    location / {
        proxy_pass http://127.0.0.1:8004;
    }
    location /static/	 {
        sendfile on;
        root /usr/share/nginx/html/django-sy-auth;
    }
    location /media/	 {
        sendfile on;
        root /usr/share/nginx/html/django-sy-auth;
    }
    location = /favicon.ico {
        sendfile on;
        root /usr/share/nginx/html/django-sy-auth/static;
    }
}
```

Дополнительно:
- [Получение сертификата для домена](https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/) - поправка: возможно, на Вашем сервере нужно вместо команды `python` использовать `python3`
