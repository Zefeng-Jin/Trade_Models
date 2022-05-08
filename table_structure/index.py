class Index:
    __slots__ = ('__index_id', '__index_type', '__index_no', '__index_name')

    # 构造函数
    def __init__(self, inxId=None, inxType=None, inxNo=None, inxNm=None, **kwargs):
        '''用双下划线开头的变量，表示私有变量，外部程序不可直接访问'''
        self.__index_id = inxId
        self.__index_type = inxType
        self.__index_no = inxNo
        self.__index_name = inxNm

    # getter
    @property
    def index_id(self):
        return self.__index_id

    # getter
    @property
    def index_type(self):
        return self.__index_type

    # getter
    @property
    def index_no(self):
        return self.__index_no

    # getter
    @property
    def index_name(self):
        return self.__index_name

    # setter
    @index_id.setter
    def index_id(self, inxId):
        self.__index_id = inxId

    # # setter
    @index_type.setter
    def index_type(self, inxType):
        self.__index_type = inxType

    # setter
    @index_name.setter
    def index_name(self, inxNo):
        self.__index_name = inxNo

    # setter
    @index_no.setter
    def index_no(self, inxNm):
        self.__index_no = inxNm

    # 相当于java的toString方法
    def __str__(self):
        return "index_id:%s index_type:%s " \
               "index_name:%s index_no:%s " % \
               (self.__index_id, self.__index_type, self.__index_name, self.__index_no)

    def __repr__(self):
        return "index_id:%s index_type:%s " \
               "index_name:%s index_no:%s " % \
               (self.__index_id, self.__index_type, self.__index_name, self.__index_no)
