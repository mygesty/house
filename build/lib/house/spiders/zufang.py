# -*- coding: utf-8 -*-
import scrapy
from ..items import HouseItem
from scrapy import Request
import re


class ZufangSpider(scrapy.Spider):
    name = 'zufang'
    allowed_domains = ['gz.zu.fang.com']
    start_urls = 'https://gz.zu.fang.com/house/i3{page}-s31/'

    def start_requests(self):
        if self.settings.get('CITY') == 'SZ':
            self.start_urls = 'https://sz.zu.fang.com/house/i3{page}-s31/'
        for i in range(1, self.settings.getint('ZUFANG_PAGE')+1):
            yield Request(self.start_urls.format(page=i), callback=self.parse)

    def parse(self, response):
        result = response.xpath('//dl[contains(@class,"hiddenMap")]')
        for selector in result:
            item = HouseItem()
            try:
                if self.settings.get('CITY') == 'GZ':
                    item['city'] = '广州'
                elif self.settings.get('CITY') == 'SZ':
                    item['city'] = '深圳'
                item['zone'] = selector.xpath('./dd/p[3]/a[1]/span/text()').extract_first()
                item['housearea'] = int(float(selector.xpath('./dd/p[2]/text()[3]').re('([\d.]+)㎡')[0]))
                item['housetype'] = selector.xpath('./dd/p[2]/text()[2]').extract_first()
                item['price'] = int(float(selector.xpath('.//div[@class="moreInfo"]/p/span/text()').extract_first()))
                item['houseurl'] = selector.xpath('./dd/p[1]/a/@href').extract_first()
                item['houseurl'] = 'https://gz.zu.fang.com'+item['houseurl']
                item['per_price'] = int(item['price'] / item['housearea'])
                item['imgurl'] = 'https:'+selector.xpath('.//img/@src').extract_first()
                try:
                    item['housenum'] = int(re.search('(\d+)室', item['housetype']).group(1))
                except:
                    item['housenum'] = 0
            except:
                continue
            yield item
