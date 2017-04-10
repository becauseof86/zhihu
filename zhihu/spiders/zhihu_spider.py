import scrapy
import json
from scrapy.spiders import Rule
import time
import re
class ZhihuSpider(scrapy.Spider):
    name='zhihu'
    start_urls=['https://static.zhihu.com/heifetz/main.app.96aedac1d43e8facf106.js']
    custom_settings={
            "DOWNLOAD_DELAY":9,
            "CONCURRENT_REQUESTS_PER_DOMAIN":1
            }
    def parse(self,response):
        oauth=re.search(r't.CLIENT_ALIAS="(.*?)"',response.text)
        if oauth:
            oauth=oauth.group(1)
        yield scrapy.Request('https://www.zhihu.com/people/wang-xiao-feng-87/followers?page=1',self.parse_page,meta={'Authorization':'oauth '+oauth})



    def parse_page(self,response):
        print response.meta
        if 'page=1' in  response.url:
            num=response.selector.xpath("//button[@class='Button PaginationButton Button--plain'][last()]/text()").extract_first()
            if num:
                num=int(num)
                for pagenum in range(2,num+1):
                    yield scrapy.Request(url=response.url[:-1]+str(pagenum),callback=self.parse,meta=response.meta)
        hrefs=response.selector.xpath("//a[@class='UserLink-link']/@href").extract()
        hrefs=hrefs[::2]
        for href in hrefs:
            code=href[8:]
            yield scrapy.Request(url="https://www.zhihu.com/api/v4/members/"+code+"?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics",callback=self.parse_item,headers={'Authorization':response.meta['Authorization']})
            yield scrapy.Request(url="https://www.zhihu.com"+href+"/followers?page=1",callback=self.parse_page,meta=response.meta)
    def parse_item(self,response):
        jsondict=json.loads(response.text)
        return jsondict


            




