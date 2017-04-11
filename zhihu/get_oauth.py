import requests
import re
def get_oauth():

    oauth_url='https://static.zhihu.com/heifetz/main.app.96aedac1d43e8facf106.js'
    headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
            }
    response=requests.get(oauth_url,headers=headers)
    oauth=re.search(r't.CLIENT_ALIAS="(.*?)"',response.text)
    if oauth:
        oauth=oauth.group(1)
        return oauth

#print get_oauth()
