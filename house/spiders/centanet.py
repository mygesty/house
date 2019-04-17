# -*- coding: utf-8 -*-
import scrapy
from ..items import HouseItem
from scrapy_splash import SplashRequest
import re


class CentanetSpider(scrapy.Spider):
    name = 'centanet'
    allowed_domains = ['gz.centanet.com']
    start_urls = 'https://gz.centanet.com/zufang/g{page}/'

    def start_requests(self):
        if self.settings.get('CITY') == 'SZ':
            self.start_urls = 'https://sz.centanet.com/zufang/g{page}/'
        for i in range(1, self.settings.get('CENTANET_PAGE')+1):
            yield SplashRequest(self.start_urls.format(page=i), callback=self.parse, args={'wait': 0.5})

    def parse(self, response):
        result = response.xpath('//div[contains(@class,"house-item")]')
        for selector in result:
            item = HouseItem()
            try:
                if self.settings.get('CITY') == 'GZ':
                    item['city'] = '广州'
                elif self.settings.get('CITY') == 'SZ':
                    item['city'] = '深圳'
                item['zone'] = selector.xpath('.//div[contains(@class,"item-info")]/p[3]/a[1]/text()').extract_first()
                item['housearea'] = int(float(selector.xpath('.//div[contains(@class,"item-info")]/p[1]/span[4]/text()').re('([\d.]+)平')[0]))
                item['housetype'] = selector.xpath('.//div[contains(@class,"item-info")]/p[1]/span[2]/text()').extract_first()
                item['price'] = int(float(selector.xpath('.//div[contains(@class,"item-pricearea")]/p[1]/span/text()').extract_first()))
                item['houseurl'] = selector.xpath('.//h4[@class="house-title"]/a/@href').extract_first()
                item['houseurl'] = 'https://gz.centanet.com'+item['houseurl']
                item['per_price'] = int(item['price'] / item['housearea'])
                item['imgurl'] = selector.xpath('.//img[@class="lazy"]/@data-original').extract_first()
                try:
                    item['housenum'] = int(re.search('(\d+)室', item['housetype']).group(1))
                except:
                    item['housenum'] = 0
            except:
                continue
            yield item
