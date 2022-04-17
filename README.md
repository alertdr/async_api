# Проектная работа 4 спринта

Используемая версия интерпритатора: python 3.10.2

## Запуск проекта
Для запуска проекта выполните команду
> docker-compose up -d

### Применение миграций
Необходимо зайти в контейнер
> docker exec -it django bash

И выполнить
> python manage.py migrate
>
> python manage.py makemigrations
