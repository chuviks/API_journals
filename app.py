from aiohttp import web
from tortoise.contrib.aiohttp import register_tortoise
from models import Building, Floor, Room, Equipment, RoomType

# Инициализация приложения
app = web.Application()

# CRUD операции для Buildings, Floors, Rooms и Equipments

# CRUD для зданий
async def create_building(request):
    data = await request.json()
    building = await Building.create(**data)
    return web.json_response({'id': building.id})

async def get_building(request):
    building_id = request.match_info.get('id')
    building = await Building.get(id=building_id).prefetch_related('floors')
    return web.json_response({'name': building.name, 'floors': [floor.number for floor in building.floors]})

async def update_building(request):
    building_id = request.match_info.get('id')
    data = await request.json()
    await Building.filter(id=building_id).update(**data)
    return web.json_response({'status': 'updated'})

async def delete_building(request):
    building_id = request.match_info.get('id')
    await Building.filter(id=building_id).delete()
    return web.json_response({'status': 'deleted'})

# CRUD для этажей
async def create_floor(request):
    data = await request.json()
    floor = await Floor.create(**data)
    return web.json_response({'id': floor.id})

async def get_floors_by_building(request):
    building_id = request.match_info.get('building_id')
    floors = await Floor.filter(building_id=building_id)
    return web.json_response({'floors': [{'id': floor.id, 'number': floor.number} for floor in floors]})

async def update_floor(request):
    floor_id = request.match_info.get('id')
    data = await request.json()
    # Убедимся, что id не обновляется
    if 'id' in data:
        del data['id']
    await Floor.filter(id=floor_id).update(**data)
    return web.json_response({'status': 'updated'})

async def delete_floor(request):
    floor_id = request.match_info.get('id')
    await Floor.filter(id=floor_id).delete()
    return web.json_response({'status': 'deleted'})

# CRUD для помещений
async def create_room(request):
    data = await request.json()
    room = await Room.create(**data)
    return web.json_response({'id': room.id})


async def get_rooms_by_floor(request):
    floor_id = request.match_info.get('floor_id')
    rooms = await Room.filter(floor_id=floor_id)

    # Преобразование RoomType в строку, ибо есть Enum
    rooms_data = [
        {
            'id': room.id,
            'name': room.name,
            'type': room.room_type.value  # Преобразование Enum в строку
        }
        for room in rooms
    ]
    return web.json_response({'rooms': rooms_data})

async def update_room(request):
    room_id = request.match_info.get('id')
    data = await request.json()
    # Убедимся, что id не обновляется
    if 'id' in data:
        del data['id']
    await Room.filter(id=room_id).update(**data)
    return web.json_response({'status': 'updated'})

async def delete_room(request):
    room_id = request.match_info.get('id')
    await Room.filter(id=room_id).delete()
    return web.json_response({'status': 'deleted'})


# CRUD для оборудования
async def create_equipment(request):
    data = await request.json()
    room = await Room.get(id=data['room_id'])

    # Проверка, что оборудование можно разместить только в производственном помещении
    if room.room_type != RoomType.PRODUCTION:
        return web.json_response({'error': 'Equipment can only be placed in production rooms'}, status=400)

    equipment = await Equipment.create(**data)
    return web.json_response({'id': equipment.id})

async def get_equipment_by_room(request):
    room_id = request.match_info.get('room_id')
    equipment = await Equipment.filter(room_id=room_id)
    return web.json_response({'equipment': [{'id': eq.id, 'name': eq.name} for eq in equipment]})

async def get_equipment_by_floor(request):
    floor_id = request.match_info.get('floor_id')
    rooms = await Room.filter(floor_id=floor_id)
    room_ids = [room.id for room in rooms]
    equipment = await Equipment.filter(room_id__in=room_ids)
    return web.json_response({'equipment': [{'id': eq.id, 'name': eq.name} for eq in equipment]})

async def get_equipment_by_building(request):
    building_id = request.match_info.get('building_id')
    floors = await Floor.filter(building_id=building_id)
    room_ids = [room.id for floor in floors for room in await Room.filter(floor_id=floor.id)]
    equipment = await Equipment.filter(room_id__in=room_ids)
    return web.json_response({'equipment': [{'id': eq.id, 'name': eq.name} for eq in equipment]})

async def update_equipment(request):
    equipment_id = request.match_info.get('id')
    data = await request.json()
    # Убедимся, что id не обновляется
    if 'id' in data:
        del data['id']
    await Equipment.filter(id=equipment_id).update(**data)
    return web.json_response({'status': 'updated'})

async def delete_equipment(request):
    equipment_id = request.match_info.get('id')
    await Equipment.filter(id=equipment_id).delete()
    return web.json_response({'status': 'deleted'})

async def move_equipment(request):
    data = await request.json()
    equipment_id = data['equipment_id']
    new_room_id = data['new_room_id']

    # Проверка типа помещения
    new_room = await Room.get(id=new_room_id)
    if new_room.room_type != RoomType.PRODUCTION:
        return web.json_response({'error': 'Equipment can only be moved to production rooms'}, status=400)

    # Перемещение оборудования
    equipment = await Equipment.get(id=equipment_id)
    await equipment.update_from_dict({'room_id': new_room_id})
    await equipment.save()

    return web.json_response({'status': 'moved'})

async def hello(request):
    return web.json_response({'Hello': 'user'})

# Регистрация маршрутов
#test
app.router.add_get('/', hello)

# Здания
app.router.add_post('/buildings', create_building)
app.router.add_get('/buildings/{id}', get_building)
app.router.add_put('/buildings/{id}', update_building)
app.router.add_delete('/buildings/{id}', delete_building)

# Этажи
app.router.add_post('/floors', create_floor)
app.router.add_get('/buildings/{building_id}/floors', get_floors_by_building)
app.router.add_put('/floors/{id}', update_floor)
app.router.add_delete('/floors/{id}', delete_floor)

# Помещения
app.router.add_post('/rooms', create_room)
app.router.add_get('/floors/{floor_id}/rooms', get_rooms_by_floor)
app.router.add_put('/rooms/{id}', update_room)
app.router.add_delete('/rooms/{id}', delete_room)

# Оборудование
app.router.add_post('/equipment', create_equipment)
app.router.add_get('/rooms/{room_id}/equipment', get_equipment_by_room)
app.router.add_get('/floors/{floor_id}/equipment', get_equipment_by_floor)
app.router.add_put('/equipment/{id}', update_equipment)
app.router.add_delete('/equipment/{id}', delete_equipment)
app.router.add_get('/buildings/{building_id}/equipment', get_equipment_by_building)
app.router.add_post('/move-equipment', move_equipment)


# Подключение к БД
register_tortoise(
    app, db_url="sqlite://./db.sqlite", modules={"models": ["models"]}, generate_schemas=True
)

# Запуск сервера
if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)
