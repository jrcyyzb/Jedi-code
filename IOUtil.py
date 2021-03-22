# -*- coding: utf-8 -*-
# @Author: Hugh
# @Date: 2021/3/20 13:14
# Software: PyCharm
from Global import *

import sys
trainingName = "./training-data/training-1.txt"
sys.stdin = open(trainingName, 'r')

class IOUtil:
    def __init__(self):
        self.serverTypes = []
        # 服务器型号 -> 相对应的serverType类
        self.serverTypeMap = {}
        # 虚拟机型号 -> 相对应的virtualHost类
        self.virtualHosts = {}
        # requestID -> VM型号 virtualHostName
        self.requestIDMap = {}
        # 所有请求信息
        self.allRequests = []
        # 需要输出的信息
        self.outputs = []

    def readServerTypes(self):
        serverTypeNum = int(input())
        for i in range(serverTypeNum):
            tempStr = input()
            tempStr = tempStr[1:len(tempStr)-1]
            fields = tempStr.split(",")

            name = fields[0].strip()
            coreNum = int(fields[1].strip())
            memorySize = int(fields[2].strip())
            hardwareCost = int(fields[3].strip())
            dailyCost = int(fields[4].strip())

            serverType = ServerType(name, coreNum, memorySize, hardwareCost, dailyCost)
            self.serverTypes.append(serverType)
        return serverTypeNum

    def readVirtualHosts(self):
        virtualHostNum = int(input())
        for i in range(virtualHostNum):
            tempStr = input()
            tempStr = tempStr[1:len(tempStr) - 1]
            fields = tempStr.split(",")

            name = fields[0].strip()
            coreNum = int(fields[1].strip())
            memorySize = int(fields[2].strip())
            node = int(fields[3].strip())

            virtualHost = VirtualHost(name, coreNum, memorySize, node)
            self.virtualHosts[name] = virtualHost
        return virtualHostNum

    def readRequests(self):
        requests = []
        requestNum = int(input())
        for i in range(requestNum):
            tempStr = input()
            tempStr = tempStr[1:len(tempStr) - 1]
            fields = tempStr.split(",")

            operation = fields[0].strip()
            if operation == ADD:
                virtualHostName = fields[1].strip()
                requestID = int(fields[2].strip())
                self.requestIDMap[requestID] = virtualHostName
            else:
                # 删除请求
                requestID = int(fields[1].strip())
                virtualHostName = self.requestIDMap[requestID]
            request = Request(operation, virtualHostName, requestID)
            requests.append(request)
        self.allRequests.append(requests)
        return requestNum


    def addOutput(self, s):
        self.outputs.append(s)



def readInt():
    return int(input())
