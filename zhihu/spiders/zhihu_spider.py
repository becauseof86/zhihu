import scrapy
from scrapy_redis.spiders import RedisCrawlSpider

class ZhihuSpider(RedisCrawlSpider):
    name='zhihu'

