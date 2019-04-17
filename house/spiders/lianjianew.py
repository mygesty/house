# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib.parse import urljoin
from ..items import HouseItem
import re


class LianjianewSpider(scrapy.Spider):
    name = 'lianjianew'
    allowed_domains = ['gz.lianjia.com']
    start_urls = ['https://gz.lianjia.com/zufang']

    def parse(self, response):
        zone = response.xpath('//ul[@data-target="area"]/li[@class="filter__item--level2  "]/a/@href').extract()
        for i in zone:
            yield Request(url=urljoin(self.start_urls[0], i), callback=self.parse_village)

    def parse_village(self, response):
        village = response.xpath('//ul[@data-target="area"]/li[@class="filter__item--level3  "]/a/@href').extract()
        for i in village:
            yield Request(url=urljoin(self.start_urls[0], i), callback=self.parse_page)

    def parse_page(self, response):
        total_num = int(response.xpath("//span[@class='content__title--hl']/text()").extract_first())
        if total_num > 0:
            total_page = total_num//30+1
        else:
            total_page = 0
        for page in range(1, total_page+1):
            yield Request(url=response.url+'pg{page}/#contentList'.format(page=page), callback=self.parse_room)

    def parse_room(self, response):
        result = response.xpath('//div[@class="content__list--item"]')
        for selector in result:
            item = HouseItem()

            zone = selector.xpath('.//p[@class="content__list--item--des"]/a[1]/text()').extract_first()
            url = 'https://gz.lianjia.com' + selector.xpath(
                './/p[contains(@class,"content__list--item--title")]/a/@href').extract_first()
            if zone is None:
                # yield SplashRequest(url=url, callback=self.parse_more,args={'wait': 0.5})
                continue
            if self.settings.get('CITY') == 'GZ':
                item['city'] = '广州'
            elif self.settings.get('CITY') == 'SZ':
                item['city'] = '深圳'
            item['zone'] = zone
            item['housearea'] = int(
                float(selector.xpath('.//p[@class="content__list--item--des"]/text()').re('([\d.]+)㎡')[0]))
            item['housetype'] = selector.xpath('.//p[@class="content__list--item--des"]/text()').re('\d室\d厅\d卫')[0]
            item['price'] = int(
                float(selector.xpath('.//span[@class="content__list--item-price"]/em/text()').re('\d+')[0]))
            item['houseurl'] = url
            item['per_price'] = int(item['price'] / item['housearea'])
            item['imgurl'] = selector.xpath('.//img/@src').extract_first()
            try:
                item['housenum'] = int(re.search('(\d+)室', item['housetype']).group(1))
            except:
                item['housenum'] = 0
            yield item
