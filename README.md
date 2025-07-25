# Flask Shop API

## Быстрый старт (Docker Compose)
1. Создайте `.env.docker-compose`
2. Скопируйте `.env.docker-compose.example` в `.env.docker-compose` и задайте параметры БД (или используйте переменные по умолчанию).
3. Запустите:

```bash
docker-compose up --build
```

4. Приложение будет доступно на [http://127.0.0.1:5555](http://127.0.0.1:5555)



5. PgAdmin доступен на http://127.0.0.1:81

## Переменные окружения

- `DB__NAME` — имя базы данных
- `DB__USER` — пользователь БД
- `DB__PASSWORD` — пароль БД
- `DB__PROVIDER` — провайдер для docker 
- `DB__PASSWORD` — пароль БД
- `BASE_API` — адрес API для загрузки товаров  https://bot-igor.ru/api/products
- `DB__INTERVAL_UPLOAD` — интервал фоновой загрузки данных (в минутах)


## Основные маршруты
- `/` — Данные в html

- `/api/v1/info` — текстовая сводка по данным в БД 

## Логирование

- Все логи пишутся в консоль и в файл `logs/logs.log` внутри контейнера.

## Многопоточность

- Фоновая загрузка данных из API реализована через отдельный поток.
- Flask запускается с поддержкой многопоточности (`threaded=True`).

---

