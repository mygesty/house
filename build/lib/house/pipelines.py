# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class HousePipeline(object):
    def __init__(self, mysql_url, mysql_db, mysql_username, mysql_password):
        self.mysql_url = mysql_url
        self.mysql_db = mysql_db
        self.mysql_username = mysql_username
        self.mysql_password = mysql_password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mysql_url=crawler.settings.get('MYSQL_URL'),
                   mysql_db=crawler.settings.get('MYSQL_DB'),
                   mysql_username=crawler.settings.get('MYSQL_USERNAME'),
                   mysql_password=crawler.settings.get('MYSQL_PASSWORD'))

    def open_spider(self, spider):
        try:
            self.db = pymysql.Connect(host=self.mysql_url, user=self.mysql_username, password=self.mysql_password, database=self.mysql_db)
            self.cursor = self.db.cursor()
        except pymysql.MySQLError as e:
            print(e.args)

    def process_item(self, item, spider):
        sql_query = 'insert into zufang (zone,housearea,housetype,price,per_price,houseurl,imgurl,housenum,city) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.cursor.execute(sql_query, (item['zone'],item['housearea'],item['housetype'],item['price'],item['per_price'],item['houseurl'],item['imgurl'],item['housenum'],item['city']))
            self.db.commit()
        except pymysql.MySQLError as e:
            print(e.args)
            self.db.rollback()

    def close_spider(self, spider):
        self.db.close()
