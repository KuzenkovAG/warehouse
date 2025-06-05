<!-- TOC -->
* [Разворачивание окружения](#разворачивание-окружения)
* [Локальный запуск](#локальный-запуск)
* [Проверка линтерами](#проверка-линтерами)
  * [ruff](#ruff)
  * [mypy](#mypy)
* [Swagger](#swagger)
* [Особенности реализации](#особенности-реализации)
  * [Структура БД](#структура-бд)
  * [Реализация сервиса](#реализация-сервиса)
  * [Мониторинг за сервисом](#мониторинг-за-сервисом)
  * [Кеширование](#кеширование)
<!-- TOC -->

# Разворачивание окружения
1. Установка пакетного менеджера
```ch
python3.12 -m pip install pipenv
```
2. Создание окружение
```
python3.12 -m pipenv shell
```
3. Установка зависимостей
```ch
pipenv install --ignore-pipfile 
```

# Локальный запуск
1. Перейти в папку src
2. Создать .env
```ch
cat .env.example > .env
```
3. Развернуть инфраструктуру
```ch
docker compose up -d
```
4. Запустить продюсера сообщений
```ch
pipenv run python main_producer
```
5. Создать миграции
```ch
alembic upgrade head
```
6. Развернуть view
```ch
pipenv run uvicorn main_view:app --host 0.0.0.0 --loop uvloop
```
7. Развернуть daemon
```ch
pipenv run uvicorn main_daemon:app --host 0.0.0.0 --port 8001 --loop uvloop
```

# Проверка линтерами
## ruff
```ch
ruff format . && ruff check . --fix
```
## mypy
```ch
mypy .
```

# Swagger
Доступен по адресу - http://0.0.0.0:8000/docs

# Особенности реализации
## Структура БД
- Имеет 2 таблицы:
  - movements (содержит данные о перемещении товаров)
  - warehouses (содержит данные о наличии продуктов на складах)

## Реализация сервиса
Для работы сервиса необходимо 2 инстанса - main_view.py и main_daemon.py.
1. main_view.py
- Имеет endpoint для выдачи данных по передвижениям, о продуктах
2. main_daemon.py
- Читает сообщения из очереди и сохраняет в базу
- В базе добавлены тригеры, при добавлении записи о передвижении, в таблицу о продуктах заносятся данные
3. main_producer.py
- Скрипт для наполнения данных (для ручного тестирования)

## Мониторинг за сервисом
Для проверки готовности и жизнеспособности сервиса нужно отправить запросы
```text
GET /health
GET /readyz
```
Для проверки количества прочитанных сообщений
```text
GET /metrics

movements_stored_counter - отражает количество прочитанных сообщений
```

## Кеширование
Реализовано кеширование в оперативной памяти
```python
    @AsyncCache(maxsize=settings.MOVEMENT_CACHE_SIZE, ttl=settings.MOVEMENT_CACHE_EXPIRATION)
    async def get_movement(self, item: MovementFilter) -> list[MovementOutput]:
        ...
```
