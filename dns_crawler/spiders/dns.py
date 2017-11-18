# -*- coding: utf-8 -*-
import scrapy


class DnsSpider(scrapy.Spider):
    name = 'dns'
    allowed_domains = ['www.dns-shop.ru']
    start_urls = [
        'http://www.dns-shop.ru/',
        # 'http://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/'
    ]

    def start_requests(self):

        # todo:
        # separate crawler !!
        # for get list of categories
        # 'http://www.dns-shop.ru/',
        # for cat in response.css('ul#menu-catalog div.item-wrap ')
        # ('a::attr(href)')

        for page_num in range(1, 67):
            url = f'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/?p={page_num}&i=1'
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        title = response.xpath('//h1[@class="page-title price-item-title"]/text()').extract_first()

        if title:
            # todo:
            # check output encoding
            yield {
                'title': title
            }

        else:
            for item in response.css('div.item'):
                rel_link = item.css('div.title a::attr(href)').extract_first()
                if rel_link is not None:
                    next_page = response.urljoin(rel_link)
                    yield scrapy.Request(next_page, callback=self.parse)
