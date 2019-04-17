# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    table = 'zufang'
    # define the fields for your item here like:
    zone = scrapy.Field()
    housearea = scrapy.Field()
    housetype = scrapy.Field()
    price = scrapy.Field()
    houseurl = scrapy.Field()
    per_price = scrapy.Field()
    imgurl = scrapy.Field()
    housenum = scrapy.Field()
    city = scrapy.Field()
