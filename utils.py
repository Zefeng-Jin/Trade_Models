import datetime


def time_check():
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    start_time = "21:30:00"
    end_time = "04:30:00"
    start_date_time_str = "{} {}".format(today, start_time)
    start_date_time = datetime.datetime.strptime(start_date_time_str, '%Y-%m-%d %H:%M:%S')
    end_date_time_str = "{} {}".format(today, end_time)
    end_date_time = datetime.datetime.strptime(end_date_time_str, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    return now >= start_date_time or now <= end_date_time
