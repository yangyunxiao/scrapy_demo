# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        name = ''
        return item


class ArticleMysqlPipeline(object):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            INSERT INTO article (title,url,create_date,praise_num,collect_num,tags,content,front_image_path,url_object_id,front_image_url)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,
                            (item['title'], item['url'], item['create_date'], item['praise_num'], item['collect_num'],
                             item['tags'], item['content'], item['front_image_path'], item['url_object_id'],
                             item['front_image_url']))
        self.connection.commit()

    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['PASSWORD'],
            charset="utf8",
            use_unicode=True
        )

        connection = pymysql.connect(**db_params)
        return cls(connection)


class MysqlTwistedPipeline(object):
    """
    异步插入数据库
    """
    def __init__(self, db_pools):
        self.db_pools = db_pools

    def process_item(self, item, spider):
        query = self.db_pools.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def do_insert(self, cursor, item):
        insert_sql, db_params = item.get_insert_sql()
        cursor.execute(insert_sql, db_params)

    def handle_error(self, exception, item, spider):
        print(exception)

    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['PASSWORD'],
            charset="utf8",
            use_unicode=True
        )
        #使用twisted将mysql插入变成异步执行
        db_pools = adbapi.ConnectionPool("MySQLdb", **db_params)
        return cls(db_pools)

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'front_image_url' in item:
            for ok, value in results:
                if ok and "path" in value.keys():
                    item["front_image_path"] = value.get("path")
                else :
                    item["front_image_path"] = ""
        return item

class GifImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'image_url' in item:
            for ok, value in results:
                if ok and "path" in value.keys():
                    item["image_path"] = value.get("path")
                else :
                    item["image_path"] = ""
        return item

#
#
# class MysqlPipeline(object):
#     def __init__(self):
#         self.conn = pymysql.connect('localhost', 'root', '', 'article')
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         insert_sql = """
#             insert into jobbole_article(title,url,create_date,fav_nums)
#             VALUES (%s,%s,%s,%s)
#         """
#         self.cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['fav_nums']))
#         self.conn.commit()
#
