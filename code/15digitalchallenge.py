# code by:jack chen
# 根据启发式搜索实现15数码问题的求解


import numpy as np
import pandas as pd

"""
    state:表示每一个状态的结构体
    self.prev:指向前一状态的指针
    self.now:当前状态对应的数组
"""
class state(object):
    def __init__(self, pre_state, now_state):
        self.prev = pre_state
        self.now  = now_state

class puzzle15(object):
    def __init__(self,start, opens,closed,target):
        self.__num = 0
        self.__pos = state(0, start)
        self.__open = opens
        self.__closed = closed
        self.__target = target
        self.__history = []

    # search:启发式搜索
    def search(self):
        flag = self.search_singlestep()
        while flag == 0:
            flag = self.search_singlestep()
        if flag == 1:
            self.print_route()
        else:
            print("无法到达目标")
        

    # search_singlestep:单步
    def search_singlestep(self):
        # 1.取open表中的第一个节点,第一次不用
        if self.__num != 0:
            self.__pos = self.choose()
            if type(self.__pos) is int:
                return 2
        pos_zero = np.where(self.__pos.now == 0)
        pos_x = pos_zero[0][0]
        pos_y = pos_zero[1][0]

        # 2.判断是否到达终点
        if (self.__pos.now == self.__target).all():
            return 1

        # 3.拓展子节点:在任一轴边界时只能朝一个方向拓展
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

        # 4.将节点加入history,返回0表示未到达终点
        self.__history.append(self.__pos)
        return 0


    # open_add:将子节点加入open表        
    def open_add(self, direc, pos_x, pos_y):
        add_flag = True
        # 1.在当前状态数组上交换两个数字，实现拓展
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
        # 2.若数组已经遍历过，丢弃
        for x in self.__history:
            if (additem == x.now).all():
                add_flag = False
        # 3.根据当前数组与目标数组数字的个数差分入不同list中
        if add_flag == True:
            self.__num = self.__num + 1
            temp = (additem == self.__target) 
            diff_num = pd.value_counts(temp.flatten())    
            # flatten() 多维转一维，默认按行
            # pd.value_counts只能一维数组统计
            # diff_num 是pandas特有结构，可以索引，但需注意索引是否存在
            try:
                self.__open.setdefault(diff_num[False], []).append(state(self.__pos,additem)) 
                                                          # 不要用get，用get需要加=赋值，list赋值会变None
            except KeyError:                              # 当additem与目标一致时，比较后没有false，则索引时会出现keyerror
                self.__open.setdefault(0, []).append(state(self.__pos,additem)) 

    # choose:选择下一个处理状态，决定了搜索的方向
    def choose(self):
        for i in range(17):
            temp = self.__open.get(i, 0)
            if (type(temp) is not int) and len(temp):
                return self.__open[i].pop(0)
        return 0
    
    # print_route:打印从起始到目标的轨迹
    def print_route(self):
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


if __name__ == "__main__":
    # hard
    target1 = np.asarray(
        [[1,2,3,4],
        [5,6,7,8],
        [9,10,11,12],
        [13,14,15,0]])
    # simple
    target2 = np.asarray(
        [[11, 9, 4, 15],
        [0, 5 ,3, 12],
        [1, 7, 8, 6],
        [13, 2, 10, 14]])
    start     = np.asarray(
        [[11, 9, 4, 15],
        [1, 3 ,0, 12],
        [7, 5, 8, 6],
        [13, 2, 10, 14]])
    opens = {}
    closed = []

    modle = puzzle15(start, opens, closed, target1)
    modle.search()

