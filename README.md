<!-- TOC -->
* [Установка инфраструктуры](#установка-инфраструктуры)
* [Мониторинг за сервисом](#мониторинг-за-сервисом)
* [Кеширование](#кеширование)
<!-- TOC -->


# Установка инфраструктуры
```ch
docker compose up -d
```


# Мониторинг за сервисом
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

# Кеширование
Реализовано кеширование в оперативной памяти
```python
    @AsyncCache(maxsize=settings.MOVEMENT_CACHE_SIZE, ttl=settings.MOVEMENT_CACHE_EXPIRATION)
    async def get_movement(self, item: MovementFilter) -> list[MovementOutput]:
        ...
```
