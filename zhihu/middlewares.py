# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
from scrapy import signals
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import get_oauth
from scrapy.downloadermiddlewares.httpauth import HttpAuthMiddleware
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
class UserAgentMiddlewareNew(UserAgentMiddleware):

    def process_request(self,request,spider):
        uaobject=UserAgent()
        agent=uaobject.chrome
        request.headers['User-Agent']=agent
        
class HttpAuthMiddlewareNew(HttpAuthMiddleware):

    def spider_opened(self, spider):
        auth=get_oauth.get_oauth()
        if auth:
            self.auth=auth
        else:
            raise Exception('can not get oauth')
    def process_request(self, request, spider):
        auth = getattr(self, 'auth', None)
        if auth and b'Authorization' not in request.headers:
            request.headers[b'Authorization'] = b'oauth '+auth

class HttpProxyMiddlewareNew(object):
   # def _get_proxy(self):
    #    user_pass='H4W9XP33KQ09123D:EB03BDE80E928795'
     #   creds = base64.b64encode(user_pass).strip()
      #  proxy_url='http://proxy.abuyun.com:9020'
       # return creds,proxy_url
     def process_request(self,request,spider):
         proxy_auth='Basic '+base64.b64encode('H4W9XP33KQ09123D:EB03BDE80E928795').strip()
         request.meta['proxy']='http://proxy.abuyun.com:9020'
         request.headers['Proxy-Authorization']=proxy_auth


class RedirectMiddlewareNew(RedirectMiddleware):
    def process_response(self, request, response, spider):
        if (request.meta.get('dont_redirect', False) or
                response.status in getattr(spider, 'handle_httpstatus_list', []) or
                response.status in request.meta.get('handle_httpstatus_list', []) or
                request.meta.get('handle_httpstatus_all', False)):
            return response

        allowed_status = (301,302,303, 307)
        if 'Location' not in response.headers or response.status not in allowed_status:
            return response
        if response.status in (302,):
            return_req = self._redirect(request,request,spider,response.status)
            print '-----------------'+return_req.url
            return_req.dont_filter=True
            return return_req

        location = safe_url_string(response.headers['location'])

        redirected_url = urljoin(request.url, location)

        if response.status in (301, 307) or request.method == 'HEAD':
            redirected = request.replace(url=redirected_url)
            return self._redirect(redirected, request, spider, response.status)

        redirected = self._redirect_request_using_get(request, redirected_url)
        return self._redirect(redirected, request, spider, response.status)

class ZhihuSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

        
