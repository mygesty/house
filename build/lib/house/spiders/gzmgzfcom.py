# -*- coding: utf-8 -*-
import scrapy
from ..items import HouseItem
from scrapy_splash import SplashRequest
import re
import logging as log


class GzmgzfcomSpider(scrapy.Spider):
    name = 'gzmgzfcom'
    allowed_domains = ['gz.mgzf.com']
    start_urls = 'http://gz.mgzf.com/list/pg{page}/'

    def start_requests(self):
        if self.settings.get('CITY') == 'SZ':
            self.start_urls = 'http://sz.mgzf.com/list/pg{page}/'
        for i in range(1, self.settings.getint('GZMGZFCOM_PAGE')+1):
            yield SplashRequest(self.start_urls.format(page=i), callback=self.parse, args={'wait': 3})

    def parse(self, response):
        result = response.xpath('//div[@class="small-container"]/a')

        for selector in result:
            item = HouseItem()
            try:
                if self.settings.get('CITY') == 'GZ':
                    item['city'] = '广州'
                elif self.settings.get('CITY') == 'SZ':
                    item['city'] = '深圳'
                item['zone'] = selector.xpath('./@title').re('(\S+?)区-')[0]
                item['housearea'] = int(float(selector.xpath('./@title').re('([\d.]+)㎡')[0]))
                item['housetype'] = selector.xpath('./@title').extract_first().split('-')[2]
                item['price'] = int(float(selector.xpath('.//div[@class="text-content-right"]//span/text()').extract_first()))
                item['houseurl'] = selector.xpath('./@href').extract_first()
                item['per_price'] = int(item['price'] / item['housearea'])
                item['imgurl'] = selector.xpath('.//img/@src').extract_first()
                try:
                    item['housenum'] = int(re.search('(\d+)室', item['housetype']).group(1))
                except:
                    item['housenum'] = 0
            except:
                continue
            yield item
