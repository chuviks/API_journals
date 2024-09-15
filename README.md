# Управление зданием и оборудованием

Этот проект представляет собой серверное приложение, написанное на Python с использованием библиотеки `aiohttp` для обработки HTTP-запросов и `tortoise-orm` для работы с базой данных. Приложение управляет зданиями, этажами, помещениями и оборудованием.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone <URL репозитория>
    cd <папка с проектом>
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # для Windows: .venv\Scripts\activate
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

## Запуск сервера

Для запуска сервера используйте следующую команду:

```bash
python app.py
```
# CRUD операции

## Возможные запросы Buildings

1. POST: /buildings
2. GET: /buildings/{id}
PUT: /buildings/{id}
DELETE: /buildings/{id}

## Возможные запросы Floors

POST: /floors
GET: /buildings/{building_id}/floors
PUT: /floors/{id}
DELETE: /floors/{id}

## Возможные запросы Rooms

POST: /rooms
GET: /floors/{floor_id}/rooms
PUT: /rooms/{id}
DELETE: /rooms/{id}

## Возможные запросы Equipment

POST: /equipment or /move-equipment
GET: /rooms/{room_id}/equipment or /floors/{floor_id}/equipment or /buildings/{building_id}/equipment
PUT: /equipment/{id}
DELETE: /equipment/{id}
