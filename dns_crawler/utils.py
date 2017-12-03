import datetime
from decimal import Decimal

from pony.orm import db_session, commit, desc

from dns_crawler.items import DnsCrawlerItem
from dns_crawler.models import DnsItemModel, Price


def get_last_price(item):
    qs = Price.select(lambda p: p.item == item).order_by(lambda p: desc(p.created))[:1]
    return list(qs)[0].price


def add_item_to_db(item: DnsCrawlerItem):
    datetime_now = datetime.datetime.now()
    with db_session:

        # check item already exists
        db_item = DnsItemModel.get(uuid=item['uuid'])  # name=item['name']
        if db_item is not None:
            # update opinions, comments count
            db_item.opinions = item['opinions']
            db_item.comments = item['comments']

            # add new price
            last_price = get_last_price(db_item)
            if last_price != Decimal(item['price']):
                Price(
                    item=db_item,
                    price=item['price'],
                    created=datetime_now,
                )

            commit()
            return

        # write item to DB
        dns_item_model = DnsItemModel(
            name=item['name'],
            uuid=item['uuid'],
            opinions=item['opinions'],
            comments=item['comments'],
            created=datetime_now
        )

        Price(
            item=dns_item_model,
            price=item['price'],
            created=datetime_now,
        )

        commit()
