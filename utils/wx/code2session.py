# -*- encoding=utf-8 -*-

import json
import requests
from utils import proxy
import xcxservice.settings

'''
return data 的格式
{
  "session_key": "JmRNs6uPEpFzlMRmg4NqJQ==",
  "expires_in": 7200,
  "openid": "oXSML0ZH05BItFTFILfgCGxXxxik"
}
'''


def code2session(appid, code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
             (appid, xcxservice.settings.WX_APP_SECRET, code)
    url = API + '?' + params
    response = requests.get(url=url)
    data = json.loads(response.text)
    print(data)
    return data
