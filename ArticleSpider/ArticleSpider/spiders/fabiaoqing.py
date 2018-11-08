# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ArticleSpider.items import BiaoQingItem, ArticleItemLoader


class FabiaoqingSpider(CrawlSpider):
    name = 'fabiaoqing'
    allowed_domains = ['www.fabiaoqing.com']
    start_urls = ['https://www.fabiaoqing.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/bqb/lists/page/.*'), follow=True),
        Rule(LinkExtractor(allow=r'/bqb/detail/id/.*'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/biaoqing/detail/id/.*'), callback="parse_image_detail", follow=True),
    )

    def parse_item(self, response):
        title = response.xpath('//*[@id="bqb"]/div[1]/h1/text()').extract_first()
        a_selectors = response.css('.swiper-slide.swiper-slide-active.bqpp a')

        print("parse_item title : {0} total image count {1}".format(title, len(a_selectors)))

    def parse_image_detail(self, response):
        bq_item = ArticleItemLoader(item=BiaoQingItem(), response=response)
        bq_item.add_css("image_tags", ".ui.ignored.message a::text")
        bq_item.add_css("image_url", ".biaoqingpp::attr(src)")
        bq_item = bq_item.load_item()
        yield bq_item
