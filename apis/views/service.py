from django.http import JsonResponse


from authorization.models import User
from thirdparty import juhe

from django.views import View
from django.core.cache import cache

from utils.response import CommonResponseMixin, ReturnCode
from utils.auth import already_authorized

import json

popular_stocks = [
    {
        'code': '000001',
        'name': '平安银行',
        'market': 'sz'
    },
{
        'code': '000002',
        'name': '万科',
        'market': 'sz'
    },
{
        'code': '600036',
        'name': '招商银行',
        'market': 'sh'
    },
{
        'code': '601398',
        'name': '工商银行',
        'market': 'sh'
    },
]


class StockView(View, CommonResponseMixin):
    def get(self, request):
        # 如登录，显示关注的股票信息
        if already_authorized(request):
            open_id = request.session.get('openid')
            user = User.objects.get(open_id=open_id)
            gids_list = json.loads(user.focus_stock)
            result = []
            for gid_list in gids_list:
                market = gid_list.get('market')
                code = gid_list.get('code')
                result.append(juhe.stock(market+code))
            data = self.wrap_json_response(data=result, code=ReturnCode.SUCCESS)
            return JsonResponse(data=data, safe=False)
        else:  # 未登录则显示热门列表的股票数据
            result = []
            for stock in popular_stocks:
                gid = stock['market'] + stock['code']
                cache_stock = cache.get(gid)
                if not cache_stock:
                    respone = juhe.stock(gid=gid)
                    cache.set(gid, respone)
                    result.append(respone)
                else:
                    result.append(cache_stock)
            data = self.wrap_json_response(data=result)
            return JsonResponse(data=data, safe=False)


class StarView(View, CommonResponseMixin):
    def get(self, request):
        if len(request.GET) == 0:
            if already_authorized(request):
                open_id = request.session.get('openid')
                user = User.objects.get(open_id=open_id)
                consNames = json.loads(user.focus_stars)
                result = []
                for consName in consNames:
                    cache_star = cache.get(consName)
                    if not cache_star:
                        star = juhe.star(consName)
                        result.append(star)
                        cache.set(consName, star, 300)
                    else:
                        result.append(cache_star)
                respone = self.wrap_json_response(data=result, code=ReturnCode.SUCCESS)
                return JsonResponse(data=respone, safe=False)
            else:
                respone = self.wrap_json_response(code=ReturnCode.FAILED)
                return JsonResponse(data=respone, safe=False)
        else:
            consName = request.GET
            cache_star = cache.get(consName)
            if not cache_star:
                respone = juhe.star(consName['consName'])
                cache.set(consName, respone, 300)
            else:
                respone = cache_star
            data = self.wrap_json_response(data=respone)
            return JsonResponse(data=data, safe=False)






