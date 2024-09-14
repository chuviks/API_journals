from tortoise import fields
from tortoise.models import Model
from enum import Enum

class Building(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

class Floor(Model):
    id = fields.IntField(pk=True)
    number = fields.IntField()
    building = fields.ForeignKeyField('models.Building', related_name='floors')

class RoomType(Enum):
    PRODUCTION = 'production'
    AUXILIARY = 'auxiliary'
    OTHER = 'other'

class Room(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    room_type = fields.CharEnumField(RoomType, max_length=50)
    floor = fields.ForeignKeyField('models.Floor', related_name='rooms')

class Equipment(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    room = fields.ForeignKeyField('models.Room', related_name='equipment')
