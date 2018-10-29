# -*- coding: utf-8 -*-
import urllib
from urllib import parse

import scrapy
import re

from scrapy import Request
from scrapy.loader import ItemLoader

from ArticleSpider.items import ArticleDetailItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/#']
    # start_urls = ['http://blog.jobbole.com/86935/']

    def parse(self, response):
        article_nodes = response.css('#archive .post.floated-thumb')
        # article_nodes = response.css('.post-meta .archive-title::attr(href)').extract()
        for article_node in article_nodes:
            post_url = article_node.css('.post-thumb a::attr(href)').extract_first()
            front_image_url = article_node.css('.post-thumb a img::attr(src)').extract_first()
            yield Request(parse.urljoin(response.url, post_url), meta={'front_image_url': parse.urljoin(response.url, front_image_url)},
                          callback=self.parse_page_detail)

        next_page_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_page_url:
            print(next_page_url)
            yield Request(parse.urljoin(response.url, next_page_url), self.parse)
        # yield Request(response.url,
        #               meta={'front_image_url': "http://blog.jobbole.com/wp-content/themes/jobboleblogv3/_assets/img/jobbole-logo.png"},
        #                   callback=self.parse_page_detail)
    def parse_page_detail(self, response):

        # title_text = response.xpath('//*[@id="post-114447"]/div[1]/h1/text()').extract()[0]
        # tag_list = response.xpath('//*[@id=\"post-114447\"]/div[2]/p/a/text()').extract()
        # text_content = response.xpath('//*[@id="post-114447"]/div[3]').extract()
        # praise_num = response.xpath('//*[@id="114447votetotal"]/text()').extract()[0]
        # collect_num = response.xpath('//*[@id="post-114447"]/div[3]/div[20]/span[2]/text()').extract()[0].strip()
        # article_item = ArticleDetailItem()
        #
        # front_image_url = response.meta.get('front_image_url', "")
        # title = response.css('.entry-header h1::text').extract_first()
        # tags = response.css('.entry-meta-hide-on-mobile a::text').extract()
        # tags = ",".join(tags)
        # text_content = response.css('.entry').extract()
        # praise_num = response.css('.post-adds h10::text').extract_first()
        # collect_num = response.css('.btn-bluet-bigger.href-style.bookmark-btn.register-user-only::text').extract_first()
        # collect_num_matcher = re.match(r".*(\d+).*", collect_num)
        # create_date = response.css('.entry-meta p::text').extract_first().replace('·', '').strip()
        # if collect_num_matcher:
        #     collect_num = collect_num_matcher.group(1)
        # else:
        #     collect_num = 0
        # article_item['collect_num'] = collect_num
        # article_item['url'] = response.url
        # article_item['front_image_url'] = [front_image_url]
        # article_item['content'] = text_content
        # article_item['tags'] = tags
        # article_item['praise_num'] = praise_num
        # article_item['create_date'] = create_date


        item_loader = ArticleItemLoader(item=ArticleDetailItem(),response=response)
        item_loader.add_css("title",".entry-header h1::text")
        item_loader.add_css("collect_num",".btn-bluet-bigger.href-style.bookmark-btn.register-user-only::text")
        item_loader.add_css("praise_num",".post-adds h10::text")
        item_loader.add_value("url",response.url)
        item_loader.add_value("front_image_url",response.meta.get('front_image_url', ""))
        item_loader.add_css("content",".entry")
        item_loader.add_css("tags",".entry-meta-hide-on-mobile a::text")
        item_loader.add_css("create_date",".entry-meta p::text")
        item_loader.add_value("url_object_id",get_md5(response.url))

        article_item = item_loader.load_item()

        yield article_item
