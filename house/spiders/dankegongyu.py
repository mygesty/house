# -*- coding: utf-8 -*-
import scrapy
from ..items import HouseItem
from scrapy import Request
import re


class DankegongyuSpider(scrapy.Spider):
    name = 'dankegongyu'
    allowed_domains = ['www.dankegongyu.com']
    start_urls = 'https://www.dankegongyu.com/room/gz?page={page}'

    def start_requests(self):
        if self.settings.get('CITY') == 'SZ':
            self.start_urls = 'https://www.dankegongyu.com/room/sz?page={page}'
        for i in range(1, self.settings.getint('DANGKEGONGYU_PAGE')+1):
            yield Request(self.start_urls.format(page=i), callback=self.parse)

    def parse(self, response):
        result = response.xpath('//div[@class="r_lbx"]')
        for selector in result:
            item = HouseItem()
            try:
                zone = selector.xpath('.//div[@class="r_lbx_cena"]/a/@title').extract_first().split(' ')[0]
                for i, v in self.settings.get('MAP_DANKE').items():
                    if zone in i:
                        zone = v
                        break
                if self.settings.get('CITY') == 'GZ':
                    item['city'] = '广州'
                elif self.settings.get('CITY') == 'SZ':
                    item['city'] = '深圳'
                item['zone'] = zone
                item['housearea'] = int(float(selector.xpath('.//div[@class="r_lbx_cenb"]/text()').re('([\d.]+)㎡')[0]))
                item['housetype'] = selector.xpath('.//div[@class="r_lbx_cena"]/a/@title').extract_first().split()[2]
                item['price'] = int(float(selector.xpath('.//div[@class="r_lbx_moneya"]//span[@class="ty_b"]/text()').re('[\d.]+')[0]))
                item['houseurl'] = selector.xpath('.//a[@class="lk_more"]/@href').extract_first()
                item['per_price'] = int(item['price'] / item['housearea'])
                item['imgurl'] = selector.xpath('.//img/@src').extract_first()
                try:
                    item['housenum'] = int(re.search('(\d+)室', item['housetype']).group(1))
                except:
                    item['housenum'] = 0
            except:
                continue
            yield item
