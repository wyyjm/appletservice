import json

from django.http import JsonResponse

from authorization.models import User
from utils.auth import already_authorized

from utils.response import wrap_json_response, ReturnCode
from utils.wx.code2session import code2session

from django.views import View
from utils.response import CommonResponseMixin


# def test_session(request):
#     request.session['message'] = 'Test Session OK'
#     response = wrap_json_response(code=ReturnCode.SUCCESS)
#     return JsonResponse(data=response, safe=False)
#
#
# def test_session2(request):
#     """
#     后端获取session内容
#     """
#     print('Success get session!', request.session.items())
#     response = wrap_json_response(code=ReturnCode.SUCCESS)
#     return JsonResponse(data=response, safe=False)

class UserView(View, CommonResponseMixin):
    def get(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED)
            return JsonResponse(data=response, safe=False)
        open_id = request.session.get('openid')
        user = User.objects.get(open_id=open_id)
        data = {}
        data['focus'] = {}
        data['focus']['city'] = json.loads(user.focus_cities)
        data['focus']['stock'] = json.loads(user.focus_stock)
        data['focus']['star'] = json.loads(user.focus_stars)
        response = self.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)

    def post(self, request):
        """
        修改用户的数据
        :param request:
        :return:
        """
        if not already_authorized(request):  # 判断是否登录
            response = self.wrap_json_response(code=ReturnCode.FAILED)
            return JsonResponse(data=response, safe=False)
        openid = request.session.get('openid')
        user = User.objects.get(open_id=openid)

        received_body = request.body.decode('utf-8')
        received_body = eval(received_body)

        cities = received_body.get('city')
        stocks = received_body.get('stock')
        stars = received_body.get('star')

        user.focus_cities = json.dumps(cities)  # 将数据重新变为json数据
        user.focus_stock = json.dumps(stocks)
        user.focus_stars = json.dumps(stars)
        user.save()

        response = self.wrap_json_response(message='modify success', code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)


def __authorize_by_code(request):
    """
    使用wx.login()得到的临时code获得微信提供的code2session接口授权
    :param request:
    :return:
    """
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    code = post_data.get('code')
    app_id = post_data.get('appId')
    nickname = post_data.get('nickname')

    response = {}
    if not code or not app_id:
        response['message'] = '参数不完整'
        response['code'] = ReturnCode.BROKEN_AUTHORIZED_DATA
        return JsonResponse(data=response, safe=False)
    data = code2session(appid=app_id, code=code)
    openid = data.get('openid')
    print('openid is ' + openid)

    if not openid:
        response = wrap_json_response(code=ReturnCode.FAILED, message='auth failed!')
        return JsonResponse(data=response, safe=False)

    # openid存在
    request.session['openid'] = openid
    request.session['is_authorized'] = True  # 是否已经认证

    # 如果成功认证，判断该用户是否在数据库中
    if not User.objects.filter(open_id=openid):  # 如果不在，将用户保存到数据库
        new_user = User(open_id=openid, nickname=nickname)
        new_user.save()
        response = wrap_json_response(code=ReturnCode.SUCCESS, message='auth success')
        print('auth is not in tables')
        return JsonResponse(data=response, safe=False)

    print('auth is in tables')
    response = wrap_json_response(code=ReturnCode.SUCCESS, message='auth success')
    return JsonResponse(data=response, safe=False)


def logout(request):
    """
    注销，小程序删除存储的Cookies
    """
    request.session.clear()
    response = {}
    response['result_code'] = 0
    response['message'] = 'logout success.'
    return JsonResponse(response, safe=False)


# 判断是否已经登陆
def get_status(request):
    print('call get_status function...')
    if already_authorized(request):
        data = {"is_authorized": 1}
    else:
        data = {"is_authorized": 0}
    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(response, safe=False)

