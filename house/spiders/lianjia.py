# -*- coding: utf-8 -*-
import scrapy
from ..items import HouseItem
from scrapy import Request
import re


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['gz.lianjia.com']
    start_urls = 'https://gz.lianjia.com/zufang/pg{page}/#contentList'

    def start_requests(self):
        if self.settings.get('CITY') == 'SZ':
            self.start_urls = 'https://sz.lianjia.com/zufang/pg{page}/#contentList'
        for i in range(1, self.settings.getint('LIANJIA_PAGE')+1):
            yield Request(self.start_urls.format(page=i), callback=self.parse)

    def parse(self, response):
        result = response.xpath('//div[@class="content__list--item"]')
        for selector in result:
            item = HouseItem()
            try:
                zone = selector.xpath('.//p[@class="content__list--item--des"]/a[1]/text()').extract_first()
                url = 'https://gz.lianjia.com'+selector.xpath('.//p[contains(@class,"content__list--item--title")]/a/@href').extract_first()
                if zone is None:
                    # yield SplashRequest(url=url, callback=self.parse_more,args={'wait': 0.5})
                    continue
                if self.settings.get('CITY') == 'GZ':
                    item['city'] = '广州'
                elif self.settings.get('CITY') == 'SZ':
                    item['city'] = '深圳'
                item['zone'] = zone
                item['housearea'] = int(float(selector.xpath('.//p[@class="content__list--item--des"]/text()').re('([\d.]+)㎡')[0]))
                item['housetype'] = selector.xpath('.//p[@class="content__list--item--des"]/text()').re('\d室\d厅\d卫')[0]
                item['price'] = int(float(selector.xpath('.//span[@class="content__list--item-price"]/em/text()').re('\d+')[0]))
                item['houseurl'] = url
                item['per_price'] = int(item['price'] / item['housearea'])
                item['imgurl'] = selector.xpath('.//img/@src').extract_first()
                try:
                    item['housenum'] = int(re.search('(\d+)室', item['housetype']).group(1))
                except:
                    item['housenum'] = 0
            except:
                continue
            yield item

    # def parse_more(self, response):
    #     result = response.xpath('//ul[@data-el="layoutList"]/li')
    #     for selector in result:
    #         item = HouseItem()
    #         try:
    #             zone = response.xpath('//*[@id="info"]/p[1]/@data-desc').re('广州市(\S+)区')[0]
    #             item['housearea'] = selector.xpath('.//p[@class="flat__layout--subtitle"]/text()').re('([\d.]+)㎡')[0]
    #             item['housetype'] = '一室'
    #             item['price'] = selector.xpath('.//span[@class="fr"]/text()').re('([\d.]+)元')[0]
    #             item['houseurl'] = response.url
    #             item['zone'] = zone
    #         except:
    #             continue
    #         yield item