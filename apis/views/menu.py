import os
import yaml

from django.http import JsonResponse

from xcxservice import settings

import utils.response


def init_app_data():
    """
    会加载我们定义的app.yaml文件
    """
    data_file = os.path.join(settings.BASE_DIR, 'app.yaml')
    with open(data_file, 'r', encoding='utf-8') as f:
        apps = yaml.load(f)
        return apps


def get_menu(request):
    """
    处理请求
    """
    global_app_data = init_app_data()
    published_app_data = global_app_data.get('published')
    response = utils.response.wrap_json_response(data=published_app_data,
                                                 code=utils.response.ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)


