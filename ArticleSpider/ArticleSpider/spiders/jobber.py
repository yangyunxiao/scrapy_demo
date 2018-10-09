# -*- coding: utf-8 -*-
import scrapy


class JobberSpider(scrapy.Spider):
    name = 'jobber'
    allowed_domains = ['blog.jobber.com']
    start_urls = ['http://blog.jobber.com/']

    def parse(self, response):
        pass
