# -*- coding: utf-8 -*-
import re
import scrapy
from pony.orm import commit, db_session

from dns_crawler.models import DnsItemModel


class TestParseSpider(scrapy.Spider):
    name = 'test_parse'
    allowed_domains = ['www.dns-shop.ru']
    start_urls = [
        'https://www.dns-shop.ru/catalog/8a9ddfba20724e77/ssd-nakopiteli/',
    ]

    def parse(self, response):
        for item in response.css('div.item'):
            title = item.css('div.title a h3::text').extract_first()
            if title is None:
                continue
            price = item.css('div.price div.price_g span::attr(data-value)').extract_first()
            social = item.css('div.social')

            tt = social.css('a.opinions-count::text').extract_first()
            opinions_count = int(tt[1:-2]) if tt else 0

            tt = social.css('a.comments-count::text').extract_first()
            comments_count = int(tt[1:-2]) if tt else 0

            link = item.css('div.title a::attr(href)').extract_first()
            uuid = re.match(r'/product/([\w\d]+)/.*', link).groups()[0]

            if title and price:

                with db_session:
                    DnsItemModel(
                        name=title,
                        uuid=uuid,
                        opinions=opinions_count,
                        comments=comments_count,
                    )
                    commit()
