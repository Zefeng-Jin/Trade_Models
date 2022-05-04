class HistMarket:
    __slots__ = ('__busi_date', '__stock_code', '__open_price',
                 '__close_price', '__high_price','__low_price',
                 '__volume', '__turnover')

    # 构造函数
    def __init__(self, dateYmd=None, stockCode=None, openPrice=None, closePrice=None,
                 highPrice=None, lowPrice=None, volume=None, turnover=None, **kwargs):
        '''用双下划线开头的变量，表示私有变量，外部程序不可直接访问'''
        self.__busi_date = dateYmd
        self.__stock_code = stockCode
        self.__open_price = openPrice
        self.__close_price = closePrice
        self.__high_price = highPrice
        self.__low_price = lowPrice
        self.__volume = volume
        self.__turnover = turnover

    # getter
    @property
    def busi_date(self):
        return self.__busi_date

    # getter
    @property
    def stock_code(self):
        return self.__stock_code

    # getter
    @property
    def open_price(self):
        return self.__open_price

    # getter
    @property
    def close_price(self):
        return self.__close_price

    # getter
    @property
    def high_price(self):
        return self.__high_price

    # getter
    @property
    def low_price(self):
        return self.__low_price

    # getter
    @property
    def volume(self):
        return self.__volume

    # getter
    @property
    def turnover(self):
        return self.__turnover

    # 相当于java的toString方法
    def __str__(self):
        return "stock_code:%s busi_date:%s " \
               "open_price:%s close_price:%s " \
               "high_price:%s low_price:%s " \
               "volume:%s occur_time:%s " % \
               (self.__stock_code, self.__busi_date,
                self.__open_price, self.__close_price,
                self.__high_price, self.__low_price,
                self.__volume, self.__turnover)

    def __repr__(self):
        return "stock_code:%s busi_date:%s " \
               "open_price:%s close_price:%s " \
               "high_price:%s low_price:%s " \
               "volume:%s occur_time:%s " % \
               (self.__stock_code, self.__busi_date,
                self.__open_price, self.__close_price,
                self.__high_price, self.__low_price,
                self.__volume, self.__turnover)
