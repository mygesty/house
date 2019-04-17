# -*- coding: utf-8 -*-

# Scrapy settings for house project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from fake_useragent import UserAgent
from sklearn.manifold import Isomap
from PIL import Image
import numpy as np
import os

ua = UserAgent()

path = os.path.abspath(".")

NUM_MAP = {-3041: "1", -251: "2", 894: "3", -2476: "4", 930: "5", 1535: "6", -2084: "7", 1410: "8", 1447: "9", 1635: "0"}
image = Image.open(path+"/zufang.png")
image_l = image.convert("L")
image_array = np.array(image_l)
image_hsplit = np.hsplit(image_array, 10)
samples = np.array([i.reshape(3600,) for i in image_hsplit])
ISO = Isomap(n_components=1, n_neighbors=9).fit(samples)



BOT_NAME = "house"

SPIDER_MODULES = ["house.spiders"]
NEWSPIDER_MODULE = "house.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = ua.random

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#   "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   # "house.middlewares.HouseSpiderMiddleware": 543,
    "scrapy_splash.SplashDeduplicateArgsMiddleware": 100,
}

DUPEFILTER_CLASS = "scrapy_splash.SplashAwareDupeFilter"

HTTPCACHE_STORAGE = "scrapy_splash.SplashAwareFSCacheStorage"

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #"house.middlewares.HouseDownloaderMiddleware": 543,
    "scrapy_splash.SplashCookiesMiddleware": 723,
    "scrapy_splash.SplashMiddleware": 725,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
  "house.pipelines.HousePipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

SCHEDULER_PERSIST = False

SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"

# REDIS HOUST & PORT
REDIS_HOST = "114.116.123.62"
REDIS_POST = 6379

# Number of Hash Functions to use, defaults to 6
BLOOMFILTER_HASH_NUMBER = 6

# Bit
BLOOMFILTER_BIT = 14


MYSQL_URL = "114.116.122.217"
MYSQL_DB = "house"
MYSQL_PASSWORD = "12345678"
MYSQL_USERNAME = "root"

SPLASH_URL = "http://114.116.122.217:8050"

CITY = 'GZ'

if CITY == 'GZ':
    ANJUKE_PAGE = 50   #50
    BAIXING_PAGE = 100   #100
    CENTANET_PAGE = 134  #134
    DANGKEGONGYU_PAGE = 122  #122
    GANJI_PAGE = 70  #70
    GZ58COM_PAGE = 100
    GZ107ROOM_PAGE = 50
    GZMGZFCOM_PAGE = 28  #28
    LIANJIA_PAGE = 100  #100 yes
    QFANG_PAGE = 32   #32
    ZIROOM_PAGE = 50  #50 yes
    ZUFANG_PAGE = 100  #100
elif CITY == 'SZ':
    ANJUKE_PAGE = 50  # 50
    BAIXING_PAGE = 100  # 100
    CENTANET_PAGE = 299  # 299
    DANGKEGONGYU_PAGE = 393  # 393
    GANJI_PAGE = 70  # 70
    GZ58COM_PAGE = 100
    GZ107ROOM_PAGE = 50
    GZMGZFCOM_PAGE = 28  # 28
    LIANJIA_PAGE = 100  # 100 yes
    QFANG_PAGE = 99  # 99
    ZIROOM_PAGE = 50  # 50 yes
    ZUFANG_PAGE = 100  # 100

import pickle

if CITY == 'GZ':
    f = open(path+'/gz.txt', 'rb')
elif CITY == 'SZ':
    f = open(path+'/sz.txt', 'rb')

data = pickle.load(f)
f.close()

MAP_DANKE = data['MAP_DANKE']

MAP_GANJI = data['MAP_GANJI']

MAP_ZIROOM = data['MAP_ZIROOM']

