import datetime
import time
import schedule
import push_service as ps
import subscribe_service as ss


def task():
    stock_list = ['gb_jpm', 'gb_aapl', 'gb_msft']
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    start_time = "21:00:00"
    date_time_str = "{} {}".format(today, start_time)
    date_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    if now >= date_time:
        try:
            market_data = ss.realtime_subscribe_stocks(stock_list)
            ps.push_service().insert_market(market_data)
            print('insert successfully {}'.format(datetime.datetime.now()))
        except:
            print("error!!!")


schedule.every(1).minutes.do(task)

while True:
    # now = datetime.datetime.now()
    # if now.strftime("%H:%m") == "17:15":
    schedule.run_pending()
    time.sleep(1)

# # every hour
# schedule.every().hour.do(task)
#
# # every daya at specific time
# schedule.every().day.at("10:30").do(task)
