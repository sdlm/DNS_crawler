# -*- coding: utf-8 -*-
import re
import scrapy

ROOT_URL = 'https://www.dns-shop.ru'


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    allowed_domains = ['www.dns-shop.ru']
    start_urls = [ROOT_URL]

    custom_settings = {
        'DOWNLOAD_DELAY': 0.4
    }

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
                count = int(re.match(r'(\d+)', text).group())
                for page_num in range(1, int(count/20.0) + 2):
                    url = response.urljoin(f'?p={page_num}&i=1')
                    yield scrapy.Request(url, callback=self.my_parse)
            else:
                msg = 'URL: ' + response.url
                print('-' * len(msg))
                print(msg)
                print('-' * len(msg))

    def my_parse(self, response):
        ...
