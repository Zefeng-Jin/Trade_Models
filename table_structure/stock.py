class Stock:
    __slots__ = ('__stock_code', '__company', '__dow', '__sp500')

    # 构造函数
    def __init__(self, stock_code=None, company=None, dow=None, sp500=None, **kwargs):
        '''用双下划线开头的变量，表示私有变量，外部程序不可直接访问'''
        self.__stock_code = stock_code
        self.__company = company
        self.__dow = dow
        self.__sp500 = sp500

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
    def dow(self):
        return self.__dow

    # getter
    @property
    def sp500(self):
        return self.__sp500

    # setter
    @stock_code.setter
    def stock_code(self, stock_code):
        self.__stock_code = stock_code

    # # setter
    @company.setter
    def company(self, company):
        self.__company = company

    # setter
    @dow.setter
    def dow(self, dow):
        self.__dow = dow

    # setter
    @sp500.setter
    def sp500(self, sp500):
        self.__sp500 = sp500

    # 相当于java的toString方法
    def __str__(self):
        return "stock_code:%s company:%s " \
               "dw:%s sp500:%s " % \
               (self.__stock_code, self.__company, self.__dow, self.__sp500)

    def __repr__(self):
        return "stock_code:%s company:%s " \
               "dw:%s sp500:%s " % \
               (self.__stock_code, self.__company, self.__dow, self.__sp500)
