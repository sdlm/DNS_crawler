# -*- coding: utf-8 -*-
import re
import traceback

import scrapy

from dns_crawler.items import DnsCrawlerItem
from dns_crawler.utils import add_item_to_db

ROOT_URL = 'https://www.dns-shop.ru'


class DnsSpider(scrapy.Spider):
    name = 'dns'
    allowed_domains = ['www.dns-shop.ru']
    start_urls = [ROOT_URL]

    def parse(self, response):
        for item in response.css('a.catalog-icon::attr(href)'):
            yield scrapy.Request(ROOT_URL + item.extract(), self.parse)

        for item in response.css('a.category-item-desktop::attr(href)'):
            url = response.urljoin(item.extract())
            yield scrapy.Request(url, callback=self.my_parse_page_items)

    def my_parse_page_items(self, response):
        is_catalog_page = False
        for item in response.css('a.category-item-desktop::attr(href)'):
            is_catalog_page = True
            url = response.urljoin(item.extract())
            yield scrapy.Request(url, callback=self.my_parse_page_items)

        if not is_catalog_page:
            text = response.css('span.count-products::text').extract_first()
            if text is not None:
                try:
                    count = int(re.match(r'(\d+)', text).group())
                except Exception:
                    print(response)
                    traceback.print_exc()
                    return
                for page_num in range(1, int(count/20.0) + 2):
                    url = response.urljoin(f'?p={page_num}&i=1')
                    yield scrapy.Request(url, callback=self.my_parse)
            else:
                msg = 'URL: ' + response.url
                print('-' * len(msg))
                print(msg)
                print('-' * len(msg))

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

    def my_parse(self, response):
        for selector in response.css('div.item'):
            item = self.parse_item(selector)
            if item:
                add_item_to_db(item)
