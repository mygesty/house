# -*- coding: utf-8 -*-
import scrapy
from ..items import HouseItem
import requests
import io
import numpy as np
from PIL import Image
from scrapy_splash import SplashRequest
import re


class ZiroomSpider(scrapy.Spider):
    name = 'ziroom'
    allowed_domains = ['gz.ziroom.com']
    start_urls = 'http://gz.ziroom.com/z/nl/z2-o2.html?p={page}'

    def start_requests(self):
        if self.settings.get('CITY') == 'SZ':
            self.start_urls = 'http://sz.ziroom.com/z/nl/z2-o2.html?p={page}'
        for i in range(1, self.settings.getint('ZIROOM_PAGE')+1):
            yield SplashRequest(self.start_urls.format(page=i), callback=self.parse, args={'wait': 2})

    def parse(self, response):
        price_num = self.parse_price(response)
        result = response.xpath('//li[@class="clearfix"]')
        for selector in result:
            item = HouseItem()
            try:
                zone = selector.xpath('.//div[@class="detail"]/p[2]/span/text()').re('线(\S+)站')[0]
                if ')' in zone:
                    zone = re.search('\)(\S+)', zone).group(1)
                for i, v in self.settings.get('MAP_ZIROOM').items():
                    if zone in i:
                        zone = v
                        break
                if self.settings.get('CITY') == 'GZ':
                    item['city'] = '广州'
                elif self.settings.get('CITY') == 'SZ':
                    item['city'] = '深圳'
                item['zone'] = zone
                item['housearea'] = int(float(selector.xpath('.//div[@class="detail"]/p[1]/span[1]/text()').re('([\d.]+) ㎡')[0]))
                item['housetype'] = selector.xpath('.//div[@class="detail"]/p[1]/span[3]/text()').extract_first()
                price1 = price_num[int(selector.xpath('.//div[@class="priceDetail"]/p[1]/span[2]/@style').re(r'(\d+)')[0])//30]
                price2 = price_num[int(selector.xpath('.//div[@class="priceDetail"]/p[1]/span[3]/@style').re(r'(\d+)')[0])//30]
                price3 = price_num[int(selector.xpath('.//div[@class="priceDetail"]/p[1]/span[4]/@style').re(r'(\d+)')[0])//30]
                price4 = price_num[int(selector.xpath('.//div[@class="priceDetail"]/p[1]/span[5]/@style').re(r'(\d+)')[0])//30]

                item['price'] = int(price1+price2+price3+price4)
                item['houseurl'] = 'http:'+selector.xpath('.//div[@class="txt"]/h3/a/@href').extract_first()
                item['per_price'] = int(item['price'] / item['housearea'])
                item['imgurl'] = 'https:'+selector.xpath('.//img/@src').extract_first()
                try:
                    item['housenum'] = int(re.search('(\d+)室', item['housetype']).group(1))
                except:
                    item['housenum'] = 0
            except:
                continue
            yield item

    def parse_price(self, response):
        image_url = 'http://'+response.xpath('//style').re(r'(static.*png)')[1]
        result = requests.get(image_url)
        result = result.content
        stream = io.BytesIO(result)
        image = Image.open(stream)
        # number = tesserocr.image_to_text(image)
        # number = re.search(r'\d+', number).group()
        image_l = image.convert('L')
        image_array = np.array(image_l)
        image_hsplit = np.hsplit(image_array, 10)
        samples = np.array([i.reshape(3600,) for i in image_hsplit])
        iso = self.settings.get('ISO')
        num_map = self.settings.get('NUM_MAP')
        num_arry = iso.transform(samples)
        price_num = []
        for i in num_arry:
            num = int(i[0])
            num_string = num_map[num]
            price_num.append(num_string)
        return price_num
