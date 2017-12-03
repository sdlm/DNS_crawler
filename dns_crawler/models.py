from datetime import datetime
from decimal import Decimal
from pony.orm import *

db = Database()


class DnsItemModel(db.Entity):
    id = PrimaryKey(int, auto=True)
    uuid = Required(str)
    name = Required(str)
    opinions = Optional(int)
    comments = Optional(int)
    prices = Set('Price')
    created = Optional(datetime)


class Price(db.Entity):
    id = PrimaryKey(int, auto=True)
    item = Required(DnsItemModel)
    price = Required(Decimal)
    created = Optional(datetime)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
