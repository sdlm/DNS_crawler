# -*- coding: utf-8 -*-
import scrapy


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    allowed_domains = ['www.dns-shop.ru']
    start_urls = ['http://www.dns-shop.ru/']

    def parse(self, response):
        for item in response.css('a.catalog-icon'):
            yield {'href': item.css('a::attr(href)').extract_first()}
