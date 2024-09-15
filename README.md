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
3. PUT: /buildings/{id}
4. DELETE: /buildings/{id}

## Возможные запросы Floors

1. POST: /floors
2. GET: /buildings/{building_id}/floors
3. PUT: /floors/{id}
4. DELETE: /floors/{id}

## Возможные запросы Rooms

1. POST: /rooms
2. GET: /floors/{floor_id}/rooms
3. PUT: /rooms/{id}
4. DELETE: /rooms/{id}

## Возможные запросы Equipment

1. POST: /equipment or /move-equipment
2. GET: /rooms/{room_id}/equipment [or] /floors/{floor_id}/equipment or /buildings/{building_id}/equipment
3. PUT: /equipment/{id}
4. DELETE: /equipment/{id}
