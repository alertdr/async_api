ETL: https://github.com/alertdr/ETL
# Проектная работа
Используемая версия интерпретатора: python 3.10.2

## Запуск проекта
Для запуска проекта выполните команду
> docker-compose --profile all up -d

Опционально: Чтобы не тратить ресурсы на запуск вспомогательных контейнеров(kibana, migrate-data, etc.) выполните команду
> docker-compose --profile core up -d
> 
> При необходимости есть возможность запустить вспомогательные контейнеры отдельно
> 
> docker-compose --profile optional up -d

Запуск dev версии
> docker-compose -f docker-compose.dev.yml up -d 

Запуск тестов
> docker-compose -f tests/functional/docker-compose.yml up --abort-on-container-exit tests

### API документация
После успешного запуска сервисов доступна [документация openapi](http://127.0.0.1/api/openapi), [json формат](http://127.0.0.1/api/openapi.json)

### Опционально: Применение миграций
Необходимо зайти в контейнер
> docker exec -it django bash

И выполнить
> python manage.py migrate
>
> python manage.py makemigrations
