import datetime as dt
from datetime import datetime
import alpaca_trade_api as tradeapi
import json
import urllib.request as request
from urllib.parse import urlencode
from table_structure.market import Market

import pytz

# authentication and connection details for paper account
api_key = 'PKARUEFU8ZDET5S1XJJZ'
api_secret = 'k9LtDIakVJl2FH7jMVtaD7Y68E7g8tmxkGIkVspw'
base_url = 'https://paper-api.alpaca.markets'

# authentication and connection details for live account
# api_key = 'AK9W46VSQW67H67630G4'
# api_secret = 'dDmEmSE0zA54riAEoEOcDE86vywCNJu8aECqb30U'
# base_url = 'https://api.alpaca.markets'

app_key = '65475'
sign = '707fdd063e617f06fbe8bc3b8b88a155'


def realtime_subscribe_stocks(stock_list):
    """
    订阅股票行情数据
    :param stock_code:
    :return:
    """
    global a_list
    stock_codes = ",".join(stock_list)
    url = 'http://api.k780.com'
    params = {
        'app': 'finance.stock_realtime',
        'stoSym': stock_codes,
        'appkey': app_key,
        'sign': sign,
        'format': 'json',
    }
    params = urlencode(params)
    f = request.urlopen('%s?%s' % (url, params))
    nowapi_call = f.read()
    # print content
    result = json.loads(nowapi_call)
    ny_time = pytz.timezone('America/New_York')
    data_list = []
    if result:
        if result['success'] != '0':
            lists = dict(result['result']['lists'])
            for s in stock_list:
                if s in lists.keys():
                    a_list = []
                    m = Market(**lists[s])
                    a_list.append(datetime.strptime(m.occur_time, '%Y-%m-%d %H:%M:%S').strftime("%Y%m%d"))
                    a_list.append(m.stock_code)
                    a_list.append(m.company)
                    a_list.append(datetime.strptime(m.occur_time, '%Y-%m-%d %H:%M:%S')
                                  .astimezone(ny_time).strptime('%Y-%m-%d %H:%M:%S'))
                    a_list.append(m.open_price)
                    a_list.append(m.high_price)
                    a_list.append(m.low_price)
                    a_list.append(m.last_price)
                    a_list.append(m.volume)
                data_list.append(a_list)
        else:
            print(result['msgid'] + ' ' + result['msg'])
    else:
        print('Request nowapi fail.')

    return tuple(data_list)


def subscribe_stocks_list():
    url = 'http://api.k780.com'
    params = {
        'app': 'finance.stock_list',
        'category': 'us',
        'appkey': app_key,
        'sign': sign,
        'format': 'json',
    }
    params = urlencode(params)
    f = request.urlopen('%s?%s' % (url, params))
    nowapi_call = f.read()
    data_list = []
    # print content
    a_result = json.loads(nowapi_call)
    if a_result:
        if a_result['success'] != '0':
            lists = a_result['result']['lists']
            for s in lists:
                s_list = [s['symbol'], s['sname']]
                data_list.append(s_list)
        else:
            print(a_result['msgid'] + ' ' + a_result['msg'])
    else:
        print('Request nowapi fail.')
    return tuple(data_list)


def trade_api():
    """
    交易接口
    :return:
    """
    api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
    return api
#
#
# def reformat_date(date):
#     """
#     规范业务日期格式
#     :param date:
#     :return:
#     """
#     numPattern = re.compile(r'\d+')
#     numList = numPattern.findall(date)
#     if len(numList) < 3:
#         getLogger('ss_log').info("日期格式错误！")
#         return np.NaN
#     rNumList = []
#     # 规范年份
#     if 4 - len(str(numList[0])) != 0:
#         year = ''.join(['20', str(numList[0])])
#         rNumList.append(year)
#     else:
#         rNumList.append(str(numList[0]))
#     # 规范月份
#     if 2 - len(str(numList[1])) != 0:
#         month = ''.join(['0', str(numList[1])])
#         rNumList.append(month)
#     else:
#         rNumList.append(str(numList[1]))
#     # 规范日
#     if 2 - len(str(numList[2])) != 0:
#         d = ''.join(['0', str(numList[2])])
#         rNumList.append(d)
#     else:
#         rNumList.append(str(numList[2]))
#     newDate = ''.join(rNumList)
#     return newDate

if __name__ == '__main__':
    ny_time = pytz.timezone('America/New_York')
    time = datetime.now().astimezone(ny_time)
    print(time)