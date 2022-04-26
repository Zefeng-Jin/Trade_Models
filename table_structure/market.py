class Market:
    # # 允许绑定的对象，只有2个属性 __name 和 __age
    __slots__ = ('__stock_code', '__company', '__open_price', '__last_price',
                 '__high_price', '__low_price', '__volume', '__occur_time')

    # 构造函数
    def __init__(self, scode, sname_eng, open_price, last_price, high_price, low_price, volume, uptime, **kwargs):
        '''用双下划线开头的变量，表示私有变量，外部程序不可直接访问'''
        self.__stock_code = scode
        self.__company = sname_eng
        self.__open_price = open_price
        self.__last_price = last_price
        self.__high_price = high_price
        self.__low_price = low_price
        self.__volume = volume
        self.__occur_time = uptime

    # getter
    @property
    def stock_code(self):
        return self.__stock_code

    # getter
    @property
    def company(self):
        return self.__company

    # getter
    @property
    def open_price(self):
        return self.__open_price

    # getter
    @property
    def last_price(self):
        return self.__last_price

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
    def occur_time(self):
        return self.__occur_time

    # 相当于java的toString方法
    def __str__(self):
        return "stock_code:%s company:%s " \
               "open_price:%s last_price:%s " \
               "high_price:%s low_price:%s " \
               "volume:%s occur_time:%s " % \
               (self.__stock_code, self.__company,
                self.__open_price, self.__last_price,
                self.__high_price, self.__low_price,
                self.__volume, self.__occur_time)

    def __repr__(self):
        return "stock_code:%s company:%s " \
               "open_price:%s last_price:%s " \
               "high_price:%s low_price:%s " \
               "volume:%s occur_time:%s " % \
               (self.__stock_code, self.__company,
                self.__open_price, self.__last_price,
                self.__high_price, self.__low_price,
                self.__volume, self.__occur_time)


if __name__ == '__main__':
    map = {"age": 5, "name": "leo", "xxxx": 88}
    print(Market(**map))
#     print(p.age)
