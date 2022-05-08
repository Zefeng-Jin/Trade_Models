class Stock:
    __slots__ = ('__stock_code', '__company', '__dow', '__sp500','__api_stock_code')

    # 构造函数
    def __init__(self, stock_code=None, company=None, dow=None, sp500=None, api_stock_code=None, **kwargs):
        '''用双下划线开头的变量，表示私有变量，外部程序不可直接访问'''
        self.__stock_code = stock_code
        self.__company = company
        self.__dow = dow
        self.__sp500 = sp500
        self.__api_stock_code = api_stock_code

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

    # getter
    @property
    def api_stock_code(self):
        return self.__api_stock_code

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

    @api_stock_code.setter
    def api_stock_code(self, api_stock_code):
        self.__api_stock_code = api_stock_code

    # 相当于java的toString方法
    def __str__(self):
        return "stock_code:%s company:%s " \
               "dw:%s sp500:%s " \
               "api_stock_code:%s" % \
               (self.__stock_code, self.__company, self.__dow, self.__sp500,self.__api_stock_code)

    def __repr__(self):
        return "stock_code:%s company:%s " \
               "dw:%s sp500:%s " \
               "api_stock_code:%s" % \
               (self.__stock_code, self.__company, self.__dow, self.__sp500,self.__api_stock_code)
