import os
import hashlib

from utils.response import ReturnCode, CommonResponseMixin
from xcxservice import settings

from django.http import JsonResponse, FileResponse

from django.views import View


class ImageListView(View, CommonResponseMixin):
    """
    返回已经备份的图片的列表
    """
    def get(self, request):
        image_files = os.listdir(settings.IMAGES_DIR)
        response_data = []
        for image_file in image_files:
            response_data.append({
                'name': image_file,
                'md5': image_file[:-4]
            })
        response_data = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response_data, safe=False)


# 使用类视图优化
class ImageView(View, CommonResponseMixin):
    """
    文件的获取、上传、删除
    """
    def get(self, request):
        md5 = request.GET.get('md5')
        imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
        if os.path.exists(imgfile):
            return FileResponse(open(imgfile, 'rb'), content_type='image/jpg')
        else:
            response = self.wrap_json_response(code=ReturnCode.RESOURCE_NOT_FOUND)
            return JsonResponse(data=response, safe=False)

    def post(self, request):
        files = request.FILES
        response = []
        for key, value in files.items():
            content = value.read()
            md5 = hashlib.md5(content).hexdigest()
            path = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
            with open(path, 'wb') as f:
                f.write(content)
            response.append({
                'name': key,
                'md5': md5
            })
            message = 'POST success'
        response = self.wrap_json_response(data=response, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(data=response, safe=False)

    def delete(self, request):
        md5 = request.GET.get('md5')
        img_name = md5 + '.jpg'
        path = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
        if os.path.exists(path):
            os.remove(path)
            msg = 'Remove success'
        else:
            msg = 'File %s not found' % img_name
        response = self.wrap_json_response(message=msg)
        return JsonResponse(data=response, safe=False)


