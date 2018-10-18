# -*- coding: utf-8 -*-
import urllib
from urllib import parse

import scrapy
import re

from scrapy import Request


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/#']

    def parse(self, response):
        article_urls = response.css('.post-meta .archive-title::attr(href)').extract()
        for article_url in article_urls:
            yield Request(article_url, self.parse_page_detail)

        next_page_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_page_url:
            print(next_page_url)
            yield Request(next_page_url,self.parse)

    def parse_page_detail(self, response):
        title_text = response.css('.entry-header h1::text').extract_first()
        # title_text = response.xpath('//*[@id="post-114447"]/div[1]/h1/text()').extract()[0]
        # tag_list = response.xpath('//*[@id=\"post-114447\"]/div[2]/p/a/text()').extract()
        tag_list = response.css('.entry-meta-hide-on-mobile a::text').extract()
        tag_str = ",".join(tag_list)
        # text_content = response.xpath('//*[@id="post-114447"]/div[3]').extract()
        text_content =  response.css('.entry').extract()
        # praise_num = response.xpath('//*[@id="114447votetotal"]/text()').extract()[0]
        praise_num = response.css('.post-adds h10::text').extract_first()
        # collect_num = response.xpath('//*[@id="post-114447"]/div[3]/div[20]/span[2]/text()').extract()[0].strip()
        collect_num = response.css('.btn-bluet-bigger.href-style.bookmark-btn.register-user-only::text').extract_first()
        collect_num_matcher = re.match(r".*(\d+).*", collect_num)
        if collect_num_matcher :
            collect_num = collect_num_matcher.group(1)
        else:
            collect_num = 0
        print("url ：{4} title : {0} , tags :{1}  ,点赞 ：{2} , 收藏数 ：{3}".format(title_text, tag_str, praise_num, collect_num,response.url))
