from pony.orm import db_session, commit

from dns_crawler.items import DnsCrawlerItem
from dns_crawler.models import DnsItemModel


def add_item_to_db(item: DnsCrawlerItem):
    with db_session:

        # check item already exists
        db_item = DnsItemModel.get(name=item['name'])
        if db_item is not None:
            return

        # write item to DB
        DnsItemModel(
            name=item['name'],
            price=item['price'],
            opinions=item['opinions'],
            comments=item['comments'],
        )
        commit()
