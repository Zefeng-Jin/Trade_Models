class Trade:
    __slots__ = ('__stock_code', '__occur_time', '__trade_signal', '__position', '__model_id')

    # 构造函数
    def __init__(self, stock_code=None, occur_time=None, trade_signal=None, position=None, model_id=None, **kwargs):
        '''用双下划线开头的变量，表示私有变量，外部程序不可直接访问'''
        self.__stock_code = stock_code
        self.__occur_time = occur_time
        self.__trade_signal = trade_signal
        self.__position = position
        self.__model_id = model_id

    # getter
    @property
    def stock_code(self):
        return self.__stock_code

    # getter
    @property
    def occur_time(self):
        return self.__occur_time

    # getter
    @property
    def trade_signal(self):
        return self.__trade_signal

    # getter
    @property
    def position(self):
        return self.__position
        # getter

    @property
    def model_id(self):
        return self.__model_id

    # setter
    @stock_code.setter
    def stock_code(self, stock_code):
        self.__stock_code = stock_code

    # # setter
    @occur_time.setter
    def occur_time(self, occur_time):
        self.__occur_time = occur_time

    # setter
    @trade_signal.setter
    def trade_signal(self, trade_signal):
        self.__trade_signal = trade_signal

    # setter
    @position.setter
    def position(self, position):
        self.__position = position

    # setter
    @model_id.setter
    def model_id(self, model_id):
        self.__model_id = model_id

    # 相当于java的toString方法
    def __str__(self):
        return "stock_code:%s occur_time:%s " \
               "trade_signal:%s position:%s " \
               "model_id: %s " % \
               (self.__stock_code, self.__occur_time, self.__trade_signal, self.__position, self.__model_id)

    def __repr__(self):
        return "stock_code:%s occur_time:%s " \
               "trade_signal:%s position:%s " \
               "model_id:%s " % \
               (self.__stock_code, self.__occur_time, self.__trade_signal, self.__position, self.__model_id)
