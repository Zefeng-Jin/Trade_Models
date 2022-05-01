import datetime
import threading
import schedule
import utils
import crawler as c
from models import MovingAverage as ma
from services import push_service as ps, subscribe_service as ss


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
    ma.MovingAverage(stock_list, art_sl).schedule()


def crawler_task():
    c.Crawler().get_data()


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


schedule.every(1).minutes.do(run_threaded, market_task)
schedule.every().day.at("09:30").do(run_threaded, model_task1)
schedule.every().day.at("10:00").do(run_threaded, crawler_task)

while True:
    schedule.run_pending()
