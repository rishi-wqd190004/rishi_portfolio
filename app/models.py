# app/models.py
import datetime
import os
from peewee import *
from playhouse.shortcuts import model_to_dict
from dotenv import load_dotenv

load_dotenv()

# Database connection setup
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    db = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    db = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

# Model(s)
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
