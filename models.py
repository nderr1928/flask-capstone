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
    last_taken = DateTimeField(default=datetime.datetime.now())
    dosage = IntegerField(default='')
    dosage_unit = CharField(default='')
    quantity_remaining = IntegerField(default='')
    user_id = ForeignKeyField(User, backref='medicines')
    drug_id = CharField()
    refill_needed = BooleanField(default=0)
    frequency_value = IntegerField(default='')
    frequency_unit = CharField(default='') 

    class Meta:
        db_table = 'medicines'
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Medicine], safe = True)

    print('Database created')
    DATABASE.close()