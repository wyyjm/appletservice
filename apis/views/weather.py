from django.http import JsonResponse

from authorization.models import User
from thirdparty import juhe

from django.views import View

from utils.response import CommonResponseMixin, ReturnCode
from utils.auth import already_authorized

import json


# def helloworld(request):
#     print('request method: ', request.method)
#     print('request META: ', request.META)
#     print('request cookie: ', request.COOKIES)
#     print('request QueryDict: ', request.GET)  # 获取url参数
#     message = {
#         'message': 'JsonResponse'
#     }
#     return JsonResponse(data=message, safe=False, status=200)


# def weather(request):
#     if request.method == 'GET':  # 注意一定要答大写
#         city = request.GET.get('city')
#         data = juhe.weather(cityname=city)
#         data['city'] = city
#         return JsonResponse(data=data, safe=False, status=200)
#     elif request.method == 'POST':
#         body = request.body
#         json_body = json.loads(body)
#         cities = json_body.get('cities')
#         result = []
#         for city in cities:
#             data_city = juhe.weather(city)
#             data_city['city'] = city
#             result.append(data_city)
#         return JsonResponse(result, safe=False, status=200)
#     else:
#         return HttpResponse('no support method!')

class WeatherView(View, CommonResponseMixin):
    def get(self, request):
        """
        登录状态的关心城市天气显示
        :param request:
        :return:
        """
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED)
            return JsonResponse(data=response, safe=False)
        open_id = request.session.get('openid')
        user = User.objects.get(open_id=open_id)
        cities = json.loads(user.focus_cities)
        result = []
        for city in cities:
            cityname = city.get('city')
            data_city = juhe.weather(cityname)
            data_city['city'] = cityname
            result.append(data_city)

        response = self.wrap_json_response(data=result, code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)

    def post(self, request):
        body = request.body
        json_body = json.loads(body)
        cities = json_body.get('cities')
        result = []
        for item in cities:
            city = item['city']
            print(city)
            data_city = juhe.weather(city)
            data_city['city'] = city
            result.append(data_city)
        print(result)
        data = self.wrap_json_response(data=result)
        return JsonResponse(data=data, safe=False)
