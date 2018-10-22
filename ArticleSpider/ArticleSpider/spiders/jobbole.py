# -*- coding: utf-8 -*-
import urllib
from urllib import parse

import scrapy
import re

from scrapy import Request

from ArticleSpider.items import ArticleDetailItem


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/#']

    def parse(self, response):
        article_nodes = response.css('.grid-8')
        # article_nodes = response.css('.post-meta .archive-title::attr(href)').extract()
        for article_node in article_nodes:
            post_url = article_node.css('.post-thumb a::attr(href)').extract_first()
            front_image_url = article_node.css('.post-thumb a img::attr(src)').extract_first()
            yield Request(parse.urljoin(response.url, post_url), meta={'front_image_url': front_image_url},
                          callback=self.parse_page_detail)

        next_page_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_page_url:
            print(next_page_url)
            yield Request(parse.urljoin(response.url, next_page_url), self.parse)

    def parse_page_detail(self, response):

        # title_text = response.xpath('//*[@id="post-114447"]/div[1]/h1/text()').extract()[0]
        # tag_list = response.xpath('//*[@id=\"post-114447\"]/div[2]/p/a/text()').extract()
        # text_content = response.xpath('//*[@id="post-114447"]/div[3]').extract()
        # praise_num = response.xpath('//*[@id="114447votetotal"]/text()').extract()[0]
        # collect_num = response.xpath('//*[@id="post-114447"]/div[3]/div[20]/span[2]/text()').extract()[0].strip()
        article_item = ArticleDetailItem()

        front_image_url = response.meta.get('front_image_url', "")
        title = response.css('.entry-header h1::text').extract_first()
        tags = response.css('.entry-meta-hide-on-mobile a::text').extract()
        tags = ",".join(tags)
        text_content = response.css('.entry').extract()
        praise_num = response.css('.post-adds h10::text').extract_first()
        collect_num = response.css('.btn-bluet-bigger.href-style.bookmark-btn.register-user-only::text').extract_first()
        collect_num_matcher = re.match(r".*(\d+).*", collect_num)
        create_date = response.css('.entry-meta p::text').extract_first().replace('·', '').strip()
        if collect_num_matcher:
            collect_num = collect_num_matcher.group(1)
        else:
            collect_num = 0

        article_item['collect_num'] = collect_num
        article_item['url'] = response.url
        article_item['front_image_url'] = [front_image_url]
        article_item['content'] = text_content
        article_item['tags'] = tags
        article_item['praise_num'] = praise_num
        article_item['create_date'] = create_date

        yield article_item
