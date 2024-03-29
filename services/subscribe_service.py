import json
import urllib.request as request
from datetime import datetime
from urllib.parse import urlencode
import alpaca_trade_api as tradeapi
import pytz
import config as c
from table_structure.market import Market
from table_structure.hist_market import HistMarket
from table_structure.index import Index


def realtime_subscribe_stocks(stock_list):
    """
    订阅股票行情数据
    :param stock_list:
    :return:
    """
    global a_list
    stock_codes = ",".join(stock_list)
    params = {
        'app': 'finance.stock_realtime',
        'stoSym': stock_codes,
        'appkey': c.app_key,
        'sign': c.sign,
        'format': 'json',
    }
    params = urlencode(params)
    f = request.urlopen('%s?%s' % (c.url, params))
    nowapi_call = f.read()
    # print content
    result = json.loads(nowapi_call)
    data_list = []
    ny_time = pytz.timezone('America/New_York')
    if result:
        if result['success'] != '0':
            lists = dict(result['result']['lists'])
            for s in stock_list:
                if s in lists.keys():
                    a_list = []
                    m = Market(**lists[s])
                    a_list.append(
                        datetime.strptime(m.occur_time, '%Y-%m-%d %H:%M:%S').astimezone(ny_time).strftime("%Y%m%d"))
                    a_list.append(m.stock_code)
                    a_list.append(m.company)
                    a_list.append(datetime.strptime(m.occur_time, '%Y-%m-%d %H:%M:%S')
                                  .astimezone(ny_time))
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


def subscribe_stocks(stock_code, date):
    """
    订阅股票历史行情数据
    :param stock_list:
    :return:
    """
    global a_list
    params = {
        'app': 'finance.stock_history',
        'stoSym': stock_code,
        'htType': 'HT1D',
        'dateYmd': date,
        'appkey': c.app_key,
        'sign': c.sign,
        'format': 'json',
    }
    params = urlencode(params)
    f = request.urlopen('%s?%s' % (c.url, params))
    nowapi_call = f.read()
    result = json.loads(nowapi_call)
    data_list = []
    if result:
        if result['success'] != '0':
            data = dict(result['result']['dtList'][0])
            a_list = []
            m = HistMarket(**data)
            a_list.append(m.busi_date)
            a_list.append(stock_code.split("_")[1].upper())
            a_list.append(m.open_price)
            a_list.append(m.close_price)
            a_list.append(m.high_price)
            a_list.append(m.low_price)
            a_list.append(m.volume)
            a_list.append(m.turnover)
            data_list.append(a_list)
        else:
            print(result['msgid'] + ' ' + result['msg'])
    else:
        print('Request nowapi fail.')

    return tuple(data_list)


def subscribe_stocks_list():
    """
    订阅股票信息
    :return:
    """
    params = {
        'app': 'finance.stock_list',
        'category': 'us',
        'appkey': c.app_key,
        'sign': c.sign,
        'format': 'json',
    }
    params = urlencode(params)
    f = request.urlopen('%s?%s' % (c.url, params))
    nowapi_call = f.read()
    data_list = []
    # print content
    a_result = json.loads(nowapi_call)
    if a_result:
        if a_result['success'] != '0':
            lists = a_result['result']['lists']
            for s in lists:
                s_list = [s['symbol'].split('_')[1].upper(), s['sname'], s['symbol']]
                data_list.append(s_list)
        else:
            print(a_result['msgid'] + ' ' + a_result['msg'])
    else:
        print('Request nowapi fail.')
    return tuple(data_list)


def subscribe_index_list():
    """
    订阅指数信息
    :return:
    """
    url = 'http://api.k780.com'
    params = {
        'app': 'finance.globalindex_giList',
        'appkey': c.app_key,
        'sign': c.sign,
        'format': 'json',
    }
    params = urlencode(params)

    f = request.urlopen('%s?%s' % (url, params))
    nowapi_call = f.read()
    # print content
    a_result = json.loads(nowapi_call)
    index_list = []
    if a_result:
        if a_result['success'] != '0':
            i_dict = dict(a_result['result']['lists'])
            for i in i_dict.keys():
                l_list = []
                index = Index(**i_dict[i])
                l_list.append(index.index_id)
                l_list.append(index.index_type)
                l_list.append(index.index_name)
                l_list.append(index.index_no)
                index_list.append(l_list)
        else:
            print(a_result['msgid'] + ' ' + a_result['msg'])
    else:
        print('Request nowapi fail.')

    return tuple(index_list)


def trade_api():
    """
    交易接口
    :return:
    """
    api = tradeapi.REST(c.api_key, c.api_secret, c.base_url, api_version='v2')
    return api