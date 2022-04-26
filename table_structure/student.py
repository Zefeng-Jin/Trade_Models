class Student:

    # 允许绑定的对象，只有2个属性 __name 和 __age
    __slots__ = ('__name', '__age')

    # 构造函数
    def __init__(self, name, age, **kwargs):
        '''用双下划线开头的变量，表示私有变量，外部程序不可直接访问'''
        self.__name = name
        self.__age = age

    # def __setattr__(self, key, value):
    #     self[key] = value

    # getter
    @property
    def name(self):
        return self.__name

    # # settter
    # @name.setter
    # def name(self, name):
    #     self.__name = name

    # getter
    @property
    def age(self):
        return self.__age

    # @age.setter
    # def age(self, age):
    #     self.__age = age

    # 相当于java的toString方法
    def __str__(self):
        return "姓名:%s 年龄%s" % (self.__name, self.__age)

    # 相当于java的toString方法
    def __repr__(self):
        return "姓名:%s 年龄%s" % (self.__name, self.__age)

    # 相当于java的equals方法
    def __eq__(self, other):
        if self.__name == other.name:  # 注意这里是改进之前的版本！！使用getter
            return True
        else:
            return False

# if __name__ == '__main__':
#     map = {"age": 5, "name": "leo", "xxxx": 88}
#     p = Student(**map)
#     print(p.age)
