import os # need to not break local
import models
import datetime
from peewee import *
from flask_login import UserMixin
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('capstone.sqlite')

class User(Model):
    email = CharField(unique = True)
    password = CharField()
    admin = BooleanField(default = 0)
    location = CharField(default = "")
    is_active = BooleanField(default=1)

    def __str__(self):
        return '<User: {}, id: {}'.format(self.email, self.id)

    def __repr__(self):
        return '<User: {}, id: {}>'.format(self.email, self.id)

    class Meta:
        db_table = 'users'
        database = DATABASE

class Medicine(Model):
    brand_name = CharField()
    last_taken = DateTimeField(default = "")
    dosage = DecimalField(decimal_places=1, default='')
    dosage_unit = CharField(default='')
    quantity_remaining = DecimalField(decimal_places=1, default='')
    userId = ForeignKeyField(User, backref='medicines')

    class Meta:
        db_table = 'medicines'
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Medicine], safe = True)

    print('Database created')
    DATABASE.close()