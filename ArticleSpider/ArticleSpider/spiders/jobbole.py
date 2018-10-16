# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/107390/']

    def parse(self, response):
        h1_e = response.xpath('//*[@id="post-107390"]/div[1]/h1')
        pass
