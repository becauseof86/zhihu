import scrapy
from scrapy_redis.spiders import RedisCrawlSpider

class ZhihuSpider(RedisCrawlSpider):
    name='zhihu'
    start_urls=['https://www.zhihu.com/people/wang-xiao-feng-87/followers?page=1']
    rules=(
        Rule(LinkExtractor(allow=('/people/'),),follow=True,callback=self.parse_item),
    )
    
    
    def parse_item(self,response):
        pass

