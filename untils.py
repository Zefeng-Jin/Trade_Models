import re

import yfinance as yf
import datetime as dt
from datetime import datetime
import alpaca_trade_api as tradeapi
import pytz

# authentication and connection details for paper account
api_key = 'PKARUEFU8ZDET5S1XJJZ'
api_secret = 'k9LtDIakVJl2FH7jMVtaD7Y68E7g8tmxkGIkVspw'
base_url = 'https://paper-api.alpaca.markets'


# authentication and connection details for live account
# api_key = 'AK9W46VSQW67H67630G4'
# api_secret = 'dDmEmSE0zA54riAEoEOcDE86vywCNJu8aECqb30U'
# base_url = 'https://api.alpaca.markets'


def subscribe(stock_code):
    """
    订阅股票行情数据
    :param stock_code:
    :return:
    """
    ny_time = pytz.timezone('America/New_York')
    end = datetime.now(ny_time)
    start = end - dt.timedelta(5)
    df = yf.download(stock_code, interval='5m', start=start, end=end)
    return df


def realtime_subscribe(stock_code):
    """
    订阅股票行情数据
    :param stock_code:
    :return:
    """
    ny_time = pytz.timezone('America/New_York')
    end = datetime.now(ny_time)
    start = end - dt.timedelta(5)
    df = yf.download(stock_code, interval='5m', start=start, end=end)
    return df


def trade_api():
    """
    交易接口
    :return:
    """
    api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
    return api


def reformat_date(date):
    """
    规范业务日期格式
    :param date:
    :return:
    """
    numPattern = re.compile(r'\d+')
    numList = numPattern.findall(date)
    if len(numList) < 3:
        getLogger('ss_log').info("日期格式错误！")
        return np.NaN
    rNumList = []
    # 规范年份
    if 4 - len(str(numList[0])) != 0:
        year = ''.join(['20', str(numList[0])])
        rNumList.append(year)
    else:
        rNumList.append(str(numList[0]))
    # 规范月份
    if 2 - len(str(numList[1])) != 0:
        month = ''.join(['0', str(numList[1])])
        rNumList.append(month)
    else:
        rNumList.append(str(numList[1]))
    # 规范日
    if 2 - len(str(numList[2])) != 0:
        d = ''.join(['0', str(numList[2])])
        rNumList.append(d)
    else:
        rNumList.append(str(numList[2]))
    newDate = ''.join(rNumList)
    return newDate

if __name__ == '__main__':
    date = datetime.now().date().strftime("%Y%m%d")


