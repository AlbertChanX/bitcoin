#!/usr/bin/env python
# -*- coding:utf-8 -*-


class bag():
    def __init__(self,weight,value):
        self.weight = weight
        self.value = value

    def knapsack(self, full_weight):  # weight value存数组
        result = [[0 for i in xrange(full_weight+1)] for i in xrange(len(self.value)+1)]
        count = len(self.weight)  # 物品个数
        for n in range(1,count+1):  # n当前最大物品个数
            for weight in range(0, full_weight+1):  # 背包内重量递增
                if self.weight[n-1] <= weight:  # 第n个背包的重量为weight[n-1]判断是否小于允许容量
                    if result[n-1][weight] < (result[n-1][weight-self.weight[n-1]]+self.value[n-1]):
                        # 如果当前物品在相同重量情况下价值更高
                        result[n][weight] = result[n-1][weight-self.weight[n-1]]+self.value[n-1]
                    else:
                        result[n][weight] = result[n-1][weight]
                else:
                    result[n][weight] = result[n-1][weight]
        for perrow in result:
            print perrow
        return result

    def find_which(self, full_weight):
        result = self.knapsack(full_weight)
        i = len(result)-1
        j = len(result[i])-1
        while i >= 1:
            while j >= 1:
                if result[i-1][j]!=result[i][j]:  # 说明当前行的东西拿了
                    print '第'+ str(i)+'个'
                    j = j -self.weight[i-1]
                    i = i - 1
                    break
                else:
                    i = i -1


def main():
    sort_instance = bag([2,2,6,5,4,1,2,7,5,7,4],[6,3,5,4,6,1,4,7,3,6,1])  # 重量，价值初始化
    sort_instance.find_which(30)  # 定义背包总重量
# 4 5 7 2 2 6 4
if __name__ =='__main__':
    main()