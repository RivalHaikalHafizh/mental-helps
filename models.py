import datetime
from peewee import *

DATABASE =SqliteDatabase('mental.db')

class BaseModel(Model):
    class Meta:
        database =DATABASE

class User(BaseModel):
    email=CharField(unique=True)
    username=CharField()
    password=CharField()

class Message(BaseModel):
    # user_id=ForeignKeyField(User,backref='messages')
    content =TextField()
    published_at=DateTimeField(default=datetime.datetime.now())


class MentalHelps(BaseModel):
    Age=CharField()
    Educational_level=CharField()
    Screening_time=CharField()
    Irregular_eating_habits=CharField()
    Exercise=CharField()
    depressiveness=CharField()
    unnecessary_misunderstandings=CharField()
    online_courses=CharField()
    overthinking=CharField()
    social_media_hours=IntegerField()
    hobby_hours=IntegerField()
    increased_sleep_hours=IntegerField()
    health_problems=CharField()



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([MentalHelps,User,Message],safe=True)
    DATABASE.close()