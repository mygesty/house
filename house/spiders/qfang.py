# -*- coding: utf-8 -*-
import scrapy
from ..items import HouseItem
from scrapy_splash import SplashRequest
import re


class QfangSpider(scrapy.Spider):
    name = 'qfang'
    allowed_domains = ['guangzhou.qfang.com']
    start_urls = 'https://guangzhou.qfang.com/rent/f{page}'

    def start_requests(self):
        if self.settings.get('CITY') == 'SZ':
            self.start_urls = 'https://shenzhen.qfang.com/rent/f{page}'
        for i in range(1, self.settings.getint('QFANG_PAGE')+1):
            yield SplashRequest(self.start_urls.format(page=i), callback=self.parse, args={'wait': 3})

    def parse(self, response):
        result = response.xpath('//div[@class="house-detail"]//li[@class="clearfix"]')
        for selector in result:
            item = HouseItem()
            try:
                if self.settings.get('CITY') == 'GZ':
                    item['city'] = '广州'
                elif self.settings.get('CITY') == 'SZ':
                    item['city'] = '深圳'
                item['zone'] = selector.xpath('.//span[@class="whole-line"]/a[1]/text()').extract_first()
                item['housearea'] = int(float(selector.xpath('.//p[contains(@class,"house-about")]/span[4]/text()').re('([\d.]+)平米')[0]))
                item['housetype'] = selector.xpath('.//p[contains(@class,"house-about")]/span[2]/text()').extract_first()
                item['price'] = int(float(selector.xpath('.//div[@class="show-price"]/span/text()').extract_first()))
                item['houseurl'] = selector.xpath('.//p[@class="house-title"]/a/@href').extract_first()
                item['houseurl'] = 'https://guangzhou.qfang.com'+item['houseurl']
                item['per_price'] = int(item['price'] / item['housearea'])
                item['imgurl'] = selector.xpath('.//img/@src').extract_first()
                try:
                    item['housenum'] = int(re.search('(\d+)室', item['housetype']).group(1))
                except:
                    item['housenum'] = 0
            except:
                continue
            yield item
