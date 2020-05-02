import peewee
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('db/db.db', pragmas=(
    ('cache_size', -1024 * 128),
    ('journal_mode', 'wal'),
    ('foreign_keys', 1)))


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Vk(BaseModel):
    vk_id = peewee.CharField()
    last_seen = peewee.CharField(null=True, default=0)
    platform = peewee.IntegerField(null=True, default=0)


class Telegram(BaseModel):
    telegram_id = peewee.CharField()
    vk = peewee.ForeignKeyField(Vk, backref="telegram")


db.connect()
db.create_tables([Vk, Telegram])
