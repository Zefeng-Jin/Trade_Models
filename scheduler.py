import datetime
import threading
import schedule
import crawler as c
import utils
from models import MovingAverage as ma
from services import push_service as ps, subscribe_service as ss, query_service as qs


def market_task():
    stock_list = ['gb_jpm', 'gb_aapl', 'gb_msft']
    if utils.time_check():
        try:
            market_data = ss.realtime_subscribe_stocks(stock_list)
            ps.push_service().insert_market(market_data)
            print('insert real_market_data successfully {}'.format(datetime.datetime.now()))
        except:
            print("error!!!")


def hist_market_task():
    stock_list = ['gb_jpm', 'gb_aapl', 'gb_msft']
    yes = datetime.datetime.now() - datetime.timedelta(1)
    yes_date = yes.strftime("%Y%m%d")
    for s in stock_list:
        hist_market = ss.subscribe_stocks(s, yes_date)
        ps.push_service().insert_hist_market(hist_market)
    print('insert hist_market_data successfully {}'.format(datetime.datetime.now()))


def model_task1():
    stock_list = ['gb_jpm', 'gb_aapl', 'gb_msft']
    art_sl = 0.1
    print('start MovingAverage model {}'.format(datetime.datetime.now()))
    ma.MovingAverage(stock_list, art_sl).schedule()


def crawler_news_task():
    c.Crawler().get_data()
    print('insert news successfully {}'.format(datetime.datetime.now()))


def crawler_statistics_task():
    stock_list = [s.api_stock_code for s in qs.query_service().get_dw30()]
    c.Crawler().get_finances(stock_list)
    print('insert statistics successfully {}'.format(datetime.datetime.now()))


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


schedule.every(1).minutes.do(run_threaded, market_task)
schedule.every().day.at("09:30").do(run_threaded, hist_market_task)
schedule.every().day.at("16:10").do(run_threaded, crawler_statistics_task)
schedule.every().day.at("21:30").do(run_threaded, model_task1)
schedule.every().hours.do(run_threaded, crawler_news_task)

while True:
    schedule.run_pending()
