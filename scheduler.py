import datetime
import time
import schedule
import utils
from services import push_service as ps, subscribe_service as ss
from models import MovingAverage as ma


def market_task():
    stock_list = ['gb_jpm', 'gb_aapl', 'gb_msft']
    if utils.time_check():
        try:
            market_data = ss.realtime_subscribe_stocks(stock_list)
            ps.push_service().insert_market(market_data)
            print('insert successfully {}'.format(datetime.datetime.now()))
        except:
            print("error!!!")


def model_task1():
    stock_list = ['gb_jpm', 'gb_aapl', 'gb_msft']
    art_sl = 0.1
    executor = cf.ThreadPoolExecutor(max_workers=3)


    for s in stock_list:
        ma.MovingAverage(s, art_sl).schedule()



schedule.every(1).minutes.do(market_task)

while True:
    schedule.run_pending()
    time.sleep(1)
