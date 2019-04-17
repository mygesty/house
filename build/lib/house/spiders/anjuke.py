# -*- coding: utf-8 -*-
import scrapy
from ..items import HouseItem
from scrapy import Request
import re


class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['gz.zu.anjuke.com']
    start_urls = 'https://gz.zu.anjuke.com/fangyuan/p{page}/'

    def start_requests(self):
        if self.settings.get('CITY') == 'SZ':
            self.start_urls = 'https://sz.zu.anjuke.com/fangyuan/p{page}/'
        for i in range(1, self.settings.getint('ANJUKE_PAGE')+1):
            yield Request(self.start_urls.format(page=i), callback=self.parse)

    def parse(self, response):
        result = response.css('div.zu-itemmod')
        for selector in result:
            item = HouseItem()
            try:
                if self.settings.get('CITY') == 'GZ':
                    item['city'] = '广州'
                elif self.settings.get('CITY') == 'SZ':
                    item['city'] = '深圳'
                item['zone'] = selector.xpath('.//address[@class="details-item"]/text()').re('(\S+)-')[0]
                item['housearea'] = int(float(selector.xpath('.//p[contains(@class,"tag")]/text()[2]').re('\d+')[0]))
                item['housetype'] = selector.xpath('.//p[contains(@class,"tag")]/text()[1]').extract_first().strip()
                item['price'] = int(float(selector.xpath('.//div[@class="zu-side"]//strong/text()').extract_first()))
                item['houseurl'] = selector.xpath('.//div[@class="zu-info"]/h3/a/@href').extract_first()
                item['per_price'] = int(item['price'] / item['housearea'])
                item['imgurl'] = selector.xpath('.//img[@class="thumbnail"]/@src').extract_first()
                try:
                    item['housenum'] = int(re.search('(\d+)室', item['housetype']).group(1))
                except:
                    item['housenum'] = 0
            except:
                item['housenum'] = 0
                continue
            yield item
