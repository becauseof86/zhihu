import scrapy
import json
import time
from scrapy_redis.spiders import RedisSpider
import re
import os
class ZhihuSpider(RedisSpider):
    name='zhihu'
    #os.environ['http_proxy']='http://H4W9XP33KQ09123D:EB03BDE80E928795@proxy.abuyun.com:9020'
    #start_urls=['https://static.zhihu.com/heifetz/main.app.96aedac1d43e8facf106.js']
    def parse(self,response):
        #if 1:
            #print response.selector.xpath('//code/text()').extract_first()
            #yield scrapy.Request('http://www.ip.cn/',self.parse,dont_filter=True)
        if 'page=1' ==  response.url[-6:]:
            num=response.selector.xpath("//button[@class='Button PaginationButton Button--plain'][last()]/text()").extract_first()
            if num:
                num=int(num)
                for pagenum in range(2,num+1):
                    yield scrapy.Request(url=response.url[:-1]+str(pagenum),callback=self.parse)
        hrefs=response.selector.xpath("//a[@class='UserLink-link']/@href").extract()
        hrefs=hrefs[::2]
        for href in hrefs:
            code=href[8:]
            yield scrapy.Request(url="https://www.zhihu.com/api/v4/members/"+code+"?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics",callback=self.parse_item,priority=1)
            yield scrapy.Request(url="https://www.zhihu.com"+href+"/followers?page=1",callback=self.parse)
    def parse_item(self,response):
        jsondict=json.loads(response.text)
        return jsondict


            




