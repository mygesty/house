# -*- coding: utf-8 -*-
import scrapy
from ..items import HouseItem
from scrapy_splash import SplashRequest


class Gz107roomSpider(scrapy.Spider):
    name = 'gz107room'
    allowed_domains = ['gz.107room.com']
    start_urls = 'http://gz.107room.com/z2_a3_{page}'

    def start_requests(self):
        for i in range(1, self.settings.getint('GZ107ROOM_PAGE')+1):
            yield SplashRequest(self.start_urls.format(page=i), callback=self.parse, args={'wait': 3})

    def parse(self, response):
        result = response.xpath("//div[contains(@class,""oneHouse"")]")
        for selector in result:
            item = HouseItem()
            try:
                item['zone'] = selector.xpath('.//a[@class="houseReq"]/span[1]/text()').extract_first()
                item['housearea'] = selector.xpath('.//div[@class="res"]//p[contains(@class,"room")]/text()').extract_first()
                item['housetype'] = selector.xpath('.//a[@class="houseReq"]/span[2]/text()').extract_first()
                item['price'] = selector.xpath('.//li[@class="price"]/span/text()').extract_first()
                item['houseurl'] = selector.xpath('./a[1]/@href').extract_first()
                item['houseurl'] = 'http://gz.107room.com'+item['houseurl']
            except:
                continue
            yield item
