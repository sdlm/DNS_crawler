from decimal import Decimal
from pony.orm import *


db = Database()


class DnsItemModel(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    price = Optional(Decimal)
    opinions = Optional(int)
    comments = Optional(int)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
