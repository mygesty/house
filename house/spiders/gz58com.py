# -*- coding: utf-8 -*-
import scrapy
from ..items import HouseItem
from scrapy_splash import SplashRequest
from urllib.parse import urljoin


class Gz58comSpider(scrapy.Spider):
    name = 'gz58com'
    allowed_domains = ['gz.58.com']
    start_urls = 'https://gz.58.com/chuzu/pn{page}/'

    num_map = {'0x9fa4': '0', '0x993c': '1', '0x9f92': '2', '0x9a4b': '3', '0x9ea3': '4', '0x958f': '5', '0x9fa5': '6',
               '0x9f64': '7', '0x9476': '8', '0x9e3a': '9'}

    def start_requests(self):
        for i in range(1, self.settings.getint('GZ58COM_PAGE')+1):
            yield SplashRequest(self.start_urls.format(page=i), callback=self.parse, args={'wait': 2})

    def parse(self, response):
        result = response.xpath('//ul[@class="listUl"]/li')
        for selector in result:
            try:
                item = HouseItem()
                zone = selector.xpath('.//div[@class="des"]/p[2]/a/text()').extract_first()

                if zone is None:
                    zone = selector.xpath('.//div[@class="des"]/p[2]/text()').extract_first().split('\xa0')[0].strip()

                item['zone'] = zone

                house_info = selector.xpath('.//div[@class="des"]/p[1]/text()').extract_first()

                house_area = house_info.split('\xa0')[-1]
                item['housearea'] = self.area_parse(house_area)

                house_type = house_info.split('\xa0')[0][:6]
                item['housetype'] = self.type_parse(house_type)

                price = selector.xpath('.//div[@class="money"]/b/text()').extract_first()
                item['price'] = self.price_parse(price)

                item['houseurl'] = urljoin('https://', selector.xpath('.//div[@class="des"]/h2/a/@href').extract_first())
                yield item
            except (AttributeError, KeyError):
                continue
            finally:
                pass

    @staticmethod
    def area_parse(area):
        area_string = ''
        for i in area:
            try:
                area_string += Gz58comSpider.num_map[hex(ord(i))]
            except KeyError:
                area_string += i
            finally:
                pass
        return area_string

    @staticmethod
    def type_parse(house_type):
        type_string = ''
        for c in house_type:
            try:
                    type_string += Gz58comSpider.num_map[hex(ord(c))]
            except KeyError:
                type_string += c
            finally:
                pass
        return type_string

    @staticmethod
    def price_parse(price):
        price_string = ''
        for c in price:
            try:
                price_string += Gz58comSpider.num_map[hex(ord(c))]
            except KeyError:
                price_string += c
            finally:
                pass
        return price_string
