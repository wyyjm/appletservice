import json
import requests


def weather(cityname):
    """
    获取城市天气
    :param cityname:
    :return:
    """
    key = 'a82922893c868194bd7c2e8fce8a9c21'
    api = 'http://v.juhe.cn/weather/index'
    params = 'cityname=%s&key=%s' % (cityname, key)
    url = api + '?' + params

    # 请求url
    response = requests.get(url=url)
    # 获取json数据
    json_data = json.loads(response.text)
    # print(json_data)

    result = json_data.get('result')
    sk = result.get('sk')  # 当前天气实况

    response = dict()
    response['temp'] = sk.get('temp')  # 当前温度
    response['wind_direction'] = sk.get('wind_direction')  # 当前风向
    response['wind_strength'] = sk.get('wind_strength')  # 当前风力
    response['humidity'] = sk.get('humidity')  # 当前湿度
    response['time'] = sk.get('time')  # 当前时间

    return response


def stock(gid):
    """
    获取股票数据
    :param gid: 股票代码
    :return:
    """
    key = '3d7433eff1b64a39319d02a05565c4a6'
    api = 'http://web.juhe.cn:8080/finance/stock/hs'
    params = 'gid=%s&key=%s' % (gid, key)
    url = api + '?' + params

    response = requests.get(url=url)
    json_data = json.loads(response.text)
    json_data = json_data.get('result')[0]
    json_data = json_data.get('data')

    response = {}
    response['gid'] = gid  # 股票编号
    response['name'] = json_data['name']  # 股票名称
    response['todayStartPri'] = json_data['todayStartPri']  # 今日开盘价
    response['yestodEndPri'] = json_data['yestodEndPri']  # 昨日收盘价
    response['nowPri'] = json_data['nowPri']  # 当前价格
    response['todayMax'] = json_data['todayMax']  # 今日最高价
    response['todayMin'] = json_data['todayMin']  # 今日最低价
    response['traNumber'] = json_data['traNumber']  # 成交量
    response['traAmount'] = json_data['traAmount']  # 成交金额
    return response


def star(consName):
    """
    获取星座运势
    :param consName:
    :return:
    """
    key = '48670f13c69ea480d7033e0198554d54'
    api = 'http://web.juhe.cn:8080/constellation/getAll'
    params = 'consName=%s&key=%s' % (consName, key)
    url = api + '?' + params

    # 请求url
    response = requests.get(url=url)
    # 获取json数据
    json_data = json.loads(response.text)
    # print(json_data)

    result = json_data.get('today')

    response = dict()
    response['name'] = result.get('name')  # 星座名
    response['all'] = result.get('all')  # 综合指数
    response['color'] = result.get('color')  # 幸运色
    response['health'] = result.get('health')  # 健康指数
    response['love'] = result.get('love')  # 爱情指数
    response['money'] = result.get('money')  # 财运指数
    response['number'] = result.get('number')  # 幸运数字
    response['QFriend'] = result.get('QFriend')  # 速配星座
    response['summary'] = result.get('summary')  # 今日概述

    return response


if __name__ == '__main__':
    data = star('双子座')
    print(data)



