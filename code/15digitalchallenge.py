# code by:jack chen
# 根据启发式搜索实现15数码问题的求解


import numpy as np
import pandas as pd

class position(object):
    def __init__(self, pre_pos, now_pos, distance = 16):
        self.prev = pre_pos
        self.now  = now_pos
        self.distance = distance

class puzzle15(object):
    def __init__(self,pos, opens,closed,target):
        self.__num = 0
        # Tip:父类中初始化的隐藏属性，子类中无法访问
        # super().__init__(opens,closed,target)
        self.__pos = position(0, pos)
        self.__open = opens
        self.__closed = closed
        self.__target = target
        self.__history = []

    # search:盲目搜索
    def search(self):
        while self.search_step():
            pass
        temp = self.__pos
        route_list = [temp.now, ]
        print("可以抵达目标，路径如下：")
        while type(temp.prev) is not int:
            route_list.append(temp.prev.now) 
            temp = temp.prev
        route_list.reverse()
        for i, v in enumerate(route_list):
            print("step:{}".format(i))
            print(v)

    # search_step:盲目搜索，单步
    def search_step(self):
        # 1.取open表中的第一个节点,第一次不用
        if self.__num != 0:
            self.__pos = self.choose()
            if type(self.__pos) is int:
                print("无法到达目标")
                return 1
        # print(self.__pos)  # 记录行走轨迹
        pos_zero = np.where(self.__pos.now == 0)
        pos_x = pos_zero[0][0]
        pos_y = pos_zero[1][0]
        # 2.判断是否到达终点
        if (self.__pos.now == self.__target).all():
            # print("到达终点:")
            # print(self.__pos)
            return 0
        # 3.拓展子节点
        if pos_x == 0:
            self.open_add("x+", pos_x, pos_y)
        elif pos_x == 3:
            self.open_add("x-", pos_x, pos_y)
        else:
            self.open_add("x+", pos_x, pos_y)
            self.open_add("x-", pos_x, pos_y)
        if pos_y == 0:
            self.open_add("y+", pos_x, pos_y)
        elif pos_y == 3:
            self.open_add("y-", pos_x, pos_y)
        else:
            self.open_add("y+", pos_x, pos_y)
            self.open_add("y-", pos_x, pos_y)
        # 4.将节点加入history,返回1表示未到达终点
        self.__history.append(self.__pos)
        return 1


    # open_add:将子节点加入open表        
    def open_add(self, direc, pos_x, pos_y):
        add_flag = True
        additem = self.__pos.now.copy()
        temp = additem[pos_x, pos_y]
        if direc == "x+":
            additem[pos_x, pos_y] = additem[pos_x + 1, pos_y]
            additem[pos_x + 1, pos_y] = temp
        elif direc == "x-":
            additem[pos_x, pos_y] = additem[pos_x - 1, pos_y]
            additem[pos_x - 1, pos_y] = temp
        elif direc == "y+":
            additem[pos_x, pos_y] = additem[pos_x, pos_y + 1]
            additem[pos_x, pos_y + 1] = temp
        elif direc == "y-":
            additem[pos_x, pos_y] = additem[pos_x, pos_y - 1]
            additem[pos_x, pos_y - 1] = temp
        else:
            print("Para error at add_open")
        for x in self.__history:
            if (additem == x.now).all():
                add_flag = False
        if add_flag == True:
            self.__num = self.__num + 1
            temp = (additem == self.__target) # 加入项与目标项的不同块数
            diff_num = pd.value_counts(temp.flatten())    # flatten() 多维转一维，默认按行
                                                          # pd.value_counts只能一维数组统计
                                                          # diff_num 是pandas特有结构，可以索引
            try:
                self.__open.setdefault(diff_num[False], []).append(position(self.__pos,additem, diff_num[False])) 
                                                          # 不要用get，用get需要加=赋值，list赋值会变None
            except KeyError:                              # 当additem与目标一致时，比较后没有false，则索引时会出现keyerror
                self.__open.setdefault(0, []).append(position(self.__pos,additem, 0)) 

    # choose:选择下一个处理状态，决定了搜索的方向
    def choose(self):
        for i in range(17):
            temp = self.__open.get(i, 0)
            if (type(temp) is not int) and len(temp):
                #print("distance:{}".format(i))
                #print(self.__open)
                return self.__open[i].pop(0)
        return 0

target1 = np.asarray(
    [[1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
    [13,14,15,0]])
target2 = np.asarray(
    [[11, 9, 4, 15],
    [0, 5 ,3, 12],
    [1, 7, 8, 6],
    [13, 2, 10, 14]])
pos     = np.asarray(
    [[11, 9, 4, 15],
    [1, 3 ,0, 12],
    [7, 5, 8, 6],
    [13, 2, 10, 14]])
weight = []
obj = []
"""
for i in range(17):
    weight.append(i)
    obj.append([])
opens = dict(zip(weight, obj))
"""
opens = {}
closed = []

modle = puzzle15(pos, opens, closed, target1)
modle.search()

