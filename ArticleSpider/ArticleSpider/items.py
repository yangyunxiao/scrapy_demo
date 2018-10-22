# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    pass


class ArticleDetailItem(scrapy.Item):
    title = scrapy.Field()
    collect_num = scrapy.Field()
    praise_num = scrapy.Field()
    tags = scrapy.Field()
    create_date = scrapy.Field()
    front_image_url = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    front_image_path = scrapy.Field()
    url_object_id = scrapy.Field()
