# -*- coding: utf-8 -*-
# @Author: Hugh
# @Date: 2021/3/20 13:14
# Software: PyCharm

# 定义全局变量
global ADD, DEL, PURCHASE, MIGRATE, DEPLOY_A, DEPLOY_B, DEPLOY_AB, UNFIT
ADD = 'add'
DEL = "del"
PURCHASE = 'purchase'
MIGRATE = 'migration'
DEPLOY_A = 1
DEPLOY_B = 2
DEPLOY_AB = 3
UNFIT = 0


class ServerType:
    '''
    服务器类型信息
    '''
    def __init__(self, name, coreNum, memorySize, hardwareCost, dailyCost):
        self.name = name
        self.coreNum = coreNum
        self.memorySize = memorySize
        self.hardwareCost = hardwareCost
        self.dailyCost = dailyCost


    def __str__(self):
        return "Name:{}, coreNum:{}, memorySize:{}, hardwareCost:{}, dailyCost:{}"\
            .format(self.name, self.coreNum, self.memorySize, self.hardwareCost, self.dailyCost)


class VirtualHost:
    def __init__(self, name, coreNum, memorySize, node):
        self.name = name
        self.coreNum = coreNum
        self.memorySize = memorySize
        self.node = node    # 是否双节点部署, 0是单节点，1是双节点

    def __str__(self):
        return "Name:{}, coreNum:{}, memorySize:{}, node:{}".format(self.name,
                self.coreNum, self.memorySize, self.node)

class Request:
    def __init__(self, operation, virtualHostName, requestID):
        # 如果是del请求，则virtualHostName是对应requestID的虚拟机型号
        self.operation = operation
        self.virtualHostName = virtualHostName
        self.requestID = requestID

    def __str__(self):
        return "Operation:{}, virtualHostName:{}, requestID:{}".format(self.operation,
                    self.virtualHostName, self.requestID)


class Server:
    '''
    # 具体的服务器实例
    '''
    def __init__(self, serverType, id):
        # 在服务器集合中的下标, 即在Solver.currentServers中的下标
        self.id = id
        # 实际购买序列中的id，最后输出的id应该是这个
        self.remappedID = -1
        self.serverType = serverType
        self.A = [serverType.coreNum / 2, serverType.memorySize / 2]
        self.B = [serverType.coreNum / 2, serverType.memorySize / 2]
        # 服务器中存在的请求id，即虚拟机id
        self.requestIDs = []

    # def setServer(self, serverType, id):
    #     self.id = id
    #     self.serverType = serverType
    #     self.A = [serverType.coreNum/2, serverType.memorySize/2]
    #     self.B = [serverType.coreNum / 2, serverType.memorySize / 2]

    def fit(self, C, coreNum, memorySize):
        '''
        检查服务器的节点C是否能容纳coreNum和memorySize
        :param C: 节点A或节点B
        :param coreNum:
        :param memorySize:
        :return:
        '''
        return C[0] >= coreNum and C[1] >= memorySize
