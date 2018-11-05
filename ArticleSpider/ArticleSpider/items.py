# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from datetime import datetime
from scrapy.loader import ItemLoader
from scrapy.loader import wrap_loader_context
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.utils.datatypes import MergeDict
from scrapy.utils.misc import arg_to_iter


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def return_origin_value(value):
    return value


def get_nums(value):
    nums_matcher = re.match(r".*?(\d+).*", value)
    if nums_matcher:
        nums = int(nums_matcher.group(1))
    else:
        nums = 0
    return nums


def format_create_date(value):
    value = value.replace('·', '').strip()
    try:
        create_date = datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as ex:
        create_date = datetime.now().date()
    return create_date


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class MapComposeCustom(MapCompose):
    def __call__(self, value, loader_context=None):
        if not value:
            value.append("")
        values = arg_to_iter(value)
        if loader_context:
            context = MergeDict(loader_context, self.default_loader_context)
        else:
            context = self.default_loader_context
        wrapped_funcs = [wrap_loader_context(f, context) for f in self.functions]
        for func in wrapped_funcs:
            next_values = []
            for v in values:
                next_values += arg_to_iter(func(v))
            values = next_values
        return values


class ArticleDetailItem(scrapy.Item):
    title = scrapy.Field()
    collect_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    praise_num = scrapy.Field(
        input_processor=MapComposeCustom(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(lambda tag: "" if "评论" in "" else tag),
        output_processor=Join(",")
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(format_create_date)
    )
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_origin_value)
    )
    url = scrapy.Field()
    content = scrapy.Field()
    front_image_path = scrapy.Field(
        input_processor=MapComposeCustom(return_origin_value)
    )
    url_object_id = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO article (title,url,create_date,praise_num,collect_num,tags,content,front_image_path,url_object_id,front_image_url)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                       """
        params = (self['title'], self['url'], self['create_date'], self['praise_num'], self['collect_num'],
                  self['tags'], self['content'], self['front_image_path'], self['url_object_id'],
                  self['front_image_url'])

        return insert_sql, params


class ZhiHuQuestionItem(scrapy.Item):
    title = scrapy.Field()
    question_id = scrapy.Field()
    question_detail = scrapy.Field()
    tags = scrapy.Field(
        output_processor=Join(",")
    )
