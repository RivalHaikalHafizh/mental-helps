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
    Age=CharField()
    Educational_level=CharField()
    Screening_time=CharField()
    lack_of_practical_exposure=CharField()
    Irregular_eating_habits=CharField()
    Exercise=CharField()
    depressiveness=CharField()
    unnecessary_misunderstandings=CharField()
    online_courses=CharField()
    procrastination=IntegerField()
    social_media_hours=IntegerField()
    hobby_hours=IntegerField()
    increased_sleep_hours=IntegerField()
    online_difficulty_level=IntegerField()
    focus_level=IntegerField()
    health_problems=CharField()



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([MentalHelps,User,Message],safe=True)
    DATABASE.close()