# -*- coding: utf-8 -*-
import re

import scrapy

from dns_crawler.items import DnsCrawlerItem
from dns_crawler.utils import add_item_to_db


class TestDnsSpider(scrapy.Spider):
    name = 'test_dns'
    allowed_domains = ['www.dns-shop.ru']
    start_urls = [
        'https://www.dns-shop.ru/catalog/8a9ddfba20724e77/ssd-nakopiteli/',
    ]

    def parse_item(self, selector):
        title = selector.css('div.title a h3::text').extract_first()
        if title is None:
            return
        price = selector.css('div.price div.price_g span::attr(data-value)').extract_first()
        social = selector.css('div.social')

        tt = social.css('a.opinions-count::text').extract_first()
        opinions_count = int(tt[1:-2]) if tt else 0

        tt = social.css('a.comments-count::text').extract_first()
        comments_count = int(tt[1:-2]) if tt else 0

        link = selector.css('div.title a::attr(href)').extract_first()
        uuid = re.match(r'/product/([\w\d]+)/.*', link).groups()[0]

        if title and price:
            return DnsCrawlerItem(
                name=title,
                uuid=uuid,
                price=price,
                opinions=opinions_count,
                comments=comments_count,
            )

    def parse(self, response):
        for selector in response.css('div.item'):
            item = self.parse_item(selector)
            if item:
                add_item_to_db(item)
