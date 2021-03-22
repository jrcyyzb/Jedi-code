# -*- coding: utf-8 -*-
# @Author: Hugh
# @Date: 2021/3/20 15:25
# Software: PyCharm

from IOUtil import *


class Solver:
    def __init__(self, ioUtil, T):
        # IOUtil类
        self.ioUtil = ioUtil
        # 当前已买的服务器 [Server0, Server1, ...]，里面是服务器类
        self.currentServers = []
        # requestID -> [服务器id, 虚拟机部署方式]
        self.requestMap = {}
        # 每天要购买的服务器，serverName -> 数量，次日清空重算
        self.serversToBuy = {}
        # 当前天数
        self.currentDay = 0
        # 总天数
        self.totalDays = T
        # 购买服务器成本
        self.serverCost = 0
        # 能耗成本
        self.powerCost = 0

    def dailyRoutine(self, day):
        self.currentDay = day
        self.distribute()

    def initServerSize(self):
        '''
        将所有服务器分成三类
        :return:
        '''

    def initVirtualHostSize(self):
        '''
        将所有虚拟机分成三类
        :return:
        '''

    def getCheapestServer(self, request):
        '''
        获取 最便宜 的服务器类型
        :return: cheapestServerType, ServerType类
        '''
        minHardwareCost = 1e6
        # cheapestServerType = self.ioUtil.serverTypes[13]
        bestServerType = None
        for serverType in self.ioUtil.serverTypes:
            if serverType.hardwareCost < minHardwareCost and \
                    self.checkServerCapacity(serverType, request):
                bestServerType = serverType
                minHardwareCost = serverType.hardwareCost
        return bestServerType

    def getWeightMinServer(self, request):
        '''
        获取 权重最小 且能容纳request 的服务器类型
        :param request:
        :return:
        '''
        minWeight = 1e6
        bestServerType = None
        for serverType in self.ioUtil.serverTypes:
            weight = self.getServerWeight(serverType)
            if weight < minWeight and self.checkServerCapacity(serverType, request):
                bestServerType = serverType
                minWeight = weight
        return bestServerType

    def getServerWeight(self, serverType):
        '''
        获取serverType类型服务器的权重
        :param serverType: 一种类型的服务器， 类型：ServerType
        :return:
        '''
        # 使用该权重计算方法得到的 总成本   642994708 +  546676565  权重越小越好
        # return 0.75*serverType.coreNum + 0.22*serverType.memorySize + \
        #     serverType.hardwareCost/(serverType.coreNum*serverType.memorySize) + \
        #     0.02*serverType.dailyCost*(self.totalDays-self.currentDay)

        return 0.75 * serverType.coreNum + 0.22 * serverType.memorySize + \
               0.02 * serverType.dailyCost * (self.totalDays - self.currentDay)

        # return serverType.hardwareCost

        # return serverType.coreNum * 0.75 + serverType.memorySize * 0.22 + \
        #        serverType.hardwareCost * 0.01 + \
        #        serverType.dailyCost * 0.02 * (self.totalDays - self.currentDay)

    def displayCost(self):
        '''
        显示成本
        :return:
        '''
        print("ServerCost:{}\nPowerCost:{}\nTotalCost:{}".format(self.serverCost, self.powerCost, self.serverCost + self.powerCost))

    def purchase(self, bestServerType):
        '''
        购买服务器
        :param serverType: 要购买的服务器类， ServerType类
        :return:
        '''
        # bestServerType = self.ioUtil.serverTypes[13]

        if bestServerType.name in self.serversToBuy:
            self.serversToBuy[bestServerType.name] += 1
        else:
            self.serversToBuy[bestServerType.name] = 1
        server = Server(bestServerType, len(self.currentServers))
        self.currentServers.append(server)

    # 处理一天的请求
    def distribute(self):
        # 当天所有请求
        requests = self.ioUtil.allRequests[self.currentDay]

        # 当天之前已买服务器数量
        previousServerNum = len(self.currentServers)

        # 先处理当前请求，但是不给服务器排序
        for request in requests:
            if request.operation == ADD:
                flag = False
                while True:
                    # flag = self.match_firstfit(request)  # 首次适应法
                    flag = self.match_bestfit(request)  # 最佳适应法
                    if flag:
                        break
                    # 购买新的服务器 -- 权重最小
                    bestServerType = self.getWeightMinServer(request)
                    self.purchase(bestServerType)
            else:  # 删除请求
                # ret 是[服务器id, 部署方式]
                ret = self.requestMap[request.requestID]
                server = self.currentServers[ret[0]]
                # 要删除的虚拟机
                virtualHost = self.ioUtil.virtualHosts[request.virtualHostName]
                # 从服务器中删除虚拟机
                server.requestIDs.remove(request.requestID)
                if ret[1] == DEPLOY_AB:
                    server.A[0] += virtualHost.coreNum / 2
                    server.A[1] += virtualHost.memorySize / 2
                    server.B[0] += virtualHost.coreNum / 2
                    server.B[1] += virtualHost.memorySize / 2
                else:
                    if ret[1] == DEPLOY_A:
                        server.A[0] += virtualHost.coreNum
                        server.A[1] += virtualHost.memorySize
                    else:
                        server.B[0] += virtualHost.coreNum
                        server.B[1] += virtualHost.memorySize
        # 当天应买服务器类型数
        self.ioUtil.addOutput("(purchase, " + str(len(self.serversToBuy)) + ")")

        # 给当前要购买的服务器排序
        currentServerNum = len(self.currentServers)
        currentID = previousServerNum
        # 遍历当天要购买的服务器
        for i in range(previousServerNum, currentServerNum):
            server = self.currentServers[i]
            if server.remappedID == -1:  # 表示该服务器还未编号
                # 查询当天要购买该类型服务器数量
                num = self.serversToBuy[server.serverType.name]
                self.serverCost += server.serverType.hardwareCost * num
                self.ioUtil.addOutput("(" + server.serverType.name + ", " + str(num) + ")")
                # 给服务器编号
                for j in range(i, currentServerNum):
                    if server.serverType.name == self.currentServers[j].serverType.name:
                        self.currentServers[j].remappedID = currentID
                        currentID += 1
        self.serversToBuy.clear()

        # 迁移
        self.migrate()

        # 根据已排好序的服务器来输出
        for request in requests:
            if request.operation == ADD:
                ret = self.requestMap[request.requestID]
                server = self.currentServers[ret[0]]
                tmpStr = "(" + str(server.remappedID)
                if ret[1] == DEPLOY_AB:
                    self.ioUtil.addOutput(tmpStr + ")")
                elif ret[1] == DEPLOY_A:
                    self.ioUtil.addOutput(tmpStr + ", A)")
                else:
                    self.ioUtil.addOutput(tmpStr + ", B)")
        # 计算每日能耗成本
        for server in self.currentServers:
            if len(server.requestIDs) != 0:
                self.powerCost += server.serverType.dailyCost

    # 下次适应法、降序最佳适应法
    # 首次适应法 -- 按顺序遍历 能放下就放
    def match_firstfit(self, request):
        flag = False
        for server in self.currentServers:  # 遍历当前已有服务器
            ret = self.fitServer(server, request)
            if ret != UNFIT:
                server.requestIDs.append(request.requestID)
                self.requestMap[request.requestID] = [server.id, ret]
                flag = True
                break
        return flag

    # 最佳适应法 -- 双节点放的策略是A+B剩余最少，单节点放的策略是A/B剩余最少
    def match_bestfit(self, request):
        flag = False
        virtualHost = self.ioUtil.virtualHosts[request.virtualHostName]
        coreCost = virtualHost.coreNum
        memoryCost = virtualHost.memorySize
        minall = 999999999999
        minserver = None
        ret = None
        if virtualHost.node == 1:
            for server in self.currentServers:  # 遍历当前已有服务器 --目的是找到最合适的minserver
                coreCost /= 2
                memoryCost /= 2
                if server.fit(server.A, coreCost, memoryCost) and server.fit(server.B, coreCost, memoryCost):
                    all = server.A[0] + server.A[1] + server.B[0] + server.B[1] - coreCost * 2 - memoryCost * 2
                    if all < minall:
                        minall = all
                        minserver = server
                        flag = True
                        ret = DEPLOY_AB

        else:
            for server in self.currentServers:  # 遍历当前已有服务器 --目的是找到最合适的minserver
                if server.fit(server.A, coreCost, memoryCost):
                    all = server.A[0] + server.A[1] - coreCost - memoryCost
                    if all < minall:
                        minall = all
                        minserver = server
                        ret = DEPLOY_A
                        flag = True
                if server.fit(server.B, coreCost, memoryCost):
                    all = server.B[0] + server.B[1] - coreCost - memoryCost
                    if all < minall:
                        minall = all
                        minserver = server
                        ret = DEPLOY_B
                        flag = True

        if flag:
            if ret == DEPLOY_AB:
                minserver.A[0] -= coreCost
                minserver.A[1] -= memoryCost
                minserver.B[0] -= coreCost
                minserver.B[1] -= memoryCost
            if ret == DEPLOY_A:
                minserver.A[0] -= coreCost
                minserver.A[1] -= memoryCost
            if ret == DEPLOY_B:
                minserver.B[0] -= coreCost
                minserver.B[1] -= memoryCost
            minserver.requestIDs.append(request.requestID)
            self.requestMap[request.requestID] = [minserver.id, ret]

        return flag

    # 检查server服务器是否能放下该请求的虚拟机
    def fitServer(self, server, request):
        # 请求所对应的虚拟机
        virtualHost = self.ioUtil.virtualHosts[request.virtualHostName]
        coreCost = virtualHost.coreNum
        memoryCost = virtualHost.memorySize
        if virtualHost.node == 1:  # 双节点部署
            coreCost /= 2
            memoryCost /= 2
            fit = server.fit(server.A, coreCost, memoryCost) and \
                  server.fit(server.B, coreCost, memoryCost)
            if fit:
                server.A[0] -= coreCost
                server.A[1] -= memoryCost
                server.B[0] -= coreCost
                server.B[1] -= memoryCost
                return DEPLOY_AB
        else:
            fitA = server.fit(server.A, coreCost, memoryCost)
            if fitA:
                server.A[0] -= coreCost
                server.A[1] -= memoryCost
                return DEPLOY_A

            fitB = server.fit(server.B, coreCost, memoryCost)
            if fitB:
                server.B[0] -= coreCost
                server.B[1] -= memoryCost
                return DEPLOY_B

            # if fitA and fitB:
            #     self.getBestDeploy(server, coreCost, memoryCost)
            # elif fitA:
            #     server.A[0] -= coreCost
            #     server.A[1] -= memoryCost
            #     return DEPLOY_A
            # elif fitB:
            #     server.B[0] -= coreCost
            #     server.B[1] -= memoryCost
            #     return DEPLOY_B
        return UNFIT

    # 迁移
    def migrate(self):
        self.ioUtil.addOutput("(migration, 0)")

    # 从server的A B 节点中选出最优节点进行部署
    def getBestDeploy(self, server, coreCost, memoryCost):
        '''
        从server的A B 节点中选出最优节点进行部署
        :param server:
        :param coreCost:
        :param memoryCost:
        :return:
        '''
        arg1 = 0.25
        arg2 = 0.75
        AFree = server.A[0] * arg1 + server.A[1] * arg2
        BFree = server.B[0] * arg1 + server.B[1] * arg2
        if AFree >= BFree:
            server.A[0] -= coreCost
            server.A[1] -= memoryCost
            return DEPLOY_A
        else:
            server.B[0] -= coreCost
            server.B[1] -= memoryCost
            return DEPLOY_B

    # 检查该服务器类型是否能容纳request请求
    def checkServerCapacity(self, serverType, request):
        '''
        检查该服务器类型是否能容纳request请求
        :param serverType: ServerType类
        :param request: Request类
        :return:
        '''
        virtualHostName = self.ioUtil.requestIDMap[request.requestID]
        virtualHost = self.ioUtil.virtualHosts[virtualHostName]
        if virtualHost.node == 1:
            if serverType.coreNum >= virtualHost.coreNum and \
                    serverType.memorySize >= virtualHost.memorySize:
                return True
        else:
            if serverType.coreNum >= virtualHost.coreNum * 2 and \
                    serverType.memorySize >= virtualHost.memorySize * 2:
                return True
        return False


