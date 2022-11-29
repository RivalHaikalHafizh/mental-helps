import datetime
from peewee import *

DATABASE =SqliteDatabase('mental.db')

class BaseModel(Model):
    class Meta:
        database =DATABASE

class User(BaseModel):
    username=CharField(unique=True)
    password=CharField()

class Message(BaseModel):
    # user_id=ForeignKeyField(User,backref='messages')
    content =TextField()
    published_at=DateTimeField(default=datetime.datetime.now())


class MentalHelps(BaseModel):
    Temprature=CharField()
    Odor=CharField()
    Fat =CharField()
    Turbidity=CharField()
    merge=CharField()
    Grade=CharField()


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([MentalHelps,User,Message],safe=True)
    DATABASE.close()