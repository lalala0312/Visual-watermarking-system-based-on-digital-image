# -*- coding: utf-8 -*-
# @Time : 2022/6/26 16:24

class Content(object):
    __mes = r"https://newb.art/bouns="
    __num = 0
    __mes_list = {}

    def __init__(self):
        pass

    def get_num(self, num):
        __num = num
        for i in range(1, num+1):
            tem = self.__mes + str(i)
            self.__mes_list.update({i:tem})

    def get_mes_list(self):
        return self.__mes_list

    def print_num(self):
        print(self.__mes_list)




if __name__ == '__main__':
    p = Content()
    p.get_num(100)
    p.print_num()