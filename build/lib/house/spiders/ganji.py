# -*- coding: utf-8 -*-
import scrapy
from ..items import HouseItem
from scrapy import Request
import re


class GanjiSpider(scrapy.Spider):
    name = 'ganji'
    allowed_domains = ['gz.ganji.com']
    start_urls = 'http://gz.ganji.com/zufang/pn{page}'

    def start_requests(self):
        if self.settings.get('CITY') == 'SZ':
            self.start_urls = 'http://sz.ganji.com/zufang/pn{page}'
        for i in range(1, self.settings.getint('GANJI_PAGE')+1):
            yield Request(self.start_urls.format(page=i), callback=self.parse)

    def parse(self, response):
        result = response.xpath('//div[contains(@class,"ershoufang-list")]')
        for selector in result:
            item = HouseItem()
            try:
                zone = selector.xpath('.//dd[contains(@class,"address")][1]//a[1]/text()').extract_first().strip()
                for i, v in self.settings.get('MAP_GANJI').items():
                    if zone in i:
                        zone = v
                        break
                if self.settings.get('CITY') == 'GZ':
                    item['city'] = '广州'
                elif self.settings.get('CITY') == 'SZ':
                    item['city'] = '深圳'
                item['zone'] = zone
                item['housearea'] = int(float(selector.xpath('.//dd[contains(@class,"size")]/span[3]/text()').re('([\d.]+)㎡')[0]))
                item['housetype'] = selector.xpath('.//dd[contains(@class,"size")]/span[1]/text()').extract_first()
                item['price'] = int(float(selector.xpath('.//div[@class="price"]/span[1]/text()').extract_first()))
                item['houseurl'] = 'https:'+selector.xpath('.//dd[contains(@class,"title")]/a/@href').extract_first()
                item['per_price'] = int(item['price'] / item['housearea'])
                item['imgurl'] = selector.xpath('.//img/@src').extract_first()
                try:
                    item['housenum'] = int(re.search('(\d+)室', item['housetype']).group(1))
                except:
                    item['housenum'] = 0
            except:
                continue
            yield item
