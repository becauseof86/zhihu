import scrapy
import json
import time
from scrapy_redis.spiders import RedisSpider
import re
import math
import os
class ZhihuSpider(RedisSpider):
    name='zhihu'
    #os.environ['http_proxy']='http://H4W9XP33KQ09123D:EB03BDE80E928795@proxy.abuyun.com:9020'
    #start_urls=['https://static.zhihu.com/heifetz/main.app.96aedac1d43e8facf106.js'] to get Authorization header
    def parse(self,response):
        if 'page=1' ==  response.url[-6:]:
            pages_count=response.selector.xpath("//button[@class='Button PaginationButton Button--plain'][last()]/text()").extract_first()
            id=re.search('/people/(.*?)/followers',response.url).group(1)
            if pages_count:
                pages_count=int(pages_count)
                for page_num in range(pages_count):
                    yield scrapy.Request(url='https://www.zhihu.com/api/v4/members/'+id+'/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset='+str(page_num*20)+'&limit=20',callback=self.parse_page)
            yield scrapy.Request(url="https://www.zhihu.com/api/v4/members/"+id+"?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics",callback=self.parse_item,priority=1)
    def parse_page(self,response):
        url_token=re.findall(r'url_token": "(.*?)"',response.text)
        follower_count=re.findall(r'follower_count": (.*?),',response.text)
        zip_data=zip(url_token,follower_count)
        print zip_data
        for data in zip_data:
            id=data[0]
            if id:
                followers_count=int(data[1])
                pages_count=int(math.ceil(followers_count/20.0))
                for page_num in range(pages_count):
                    yield scrapy.Request(url='https://www.zhihu.com/api/v4/members/'+id+'/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset='+str(page_num*20)+'&limit=20',callback=self.parse_page)
                yield scrapy.Request(url="https://www.zhihu.com/api/v4/members/"+id+"?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics",callback=self.parse_item,priority=1)

    def parse_item(self,response):
        jsondict=json.loads(response.text)
        return jsondict


            




