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

Создайте файл `/etc/nginx/conf.d/auth.intera.space.conf` и запишите в него настройки для Nginx:

```
server {
    listen 80;
    listen [::]:80;
    server_name auth.intera.space www.auth.intera.space;
    root /usr/share/nginx/html/django-sy-auth;
    location / {
        proxy_pass http://127.0.0.1:8004;
    }
    location /static/ {
        sendfile on;
        root /usr/share/nginx/html/django-sy-auth;
    }
    location /media/ {
        sendfile on;
        root /usr/share/nginx/html/django-sy-auth/media;
    }
    location = /favicon.ico {
       sendfile on;
       root /usr/share/nginx/html/django-sy-auth/static;
    }
```

Если нужно установить сертификат SSL для домена, то [следуйте инструкциям](https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/) - поправка: возможно, на Вашем сервере нужно вместо команды `python` использовать `python3`.
Если Вы ранее выполняли команды из этой инструкции для других серверов Платформы, то достаточно выполнить команду `sudo certbot --nginx -d auth.intera.space -d www.auth.intera.space`, чтобы получить сертификат.
