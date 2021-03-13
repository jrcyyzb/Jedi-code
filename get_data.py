# -*- coding: utf-8 -*-
# @Author: Hugh
# @Date: 2021/3/11 18:30
# Software: PyCharm
# 获取输入数据


# 将服务器/虚拟机数据格式转化为列表
def extract(info):
    # infomation = detail.rstrip("\n")
    info = info[1:len(info)-1]
    return info.split(",")


def get_input():
    '''
    输入
    :return:
        N:  可以采购的服务器类型数量, int
        servers:  所有服务器类型信息, dict.
            {'第一种服务器类型型号':[cpu核数,内存大小,硬件成本,每日能耗成本], '第二种...':..., ...}
        M:  售卖的虚拟机类型数量, int
        virtualMachines:  所有虚拟机类型信息, dict
            {'第一种虚拟机型号':[cpu核数,内存大小,是否双节点部署], '第二种...':...}
            注：若虚拟机是双节点部署，则列表格式为：[cpu核数/2, 内存大小/2, 1, cpu核数/2, 内存大小/2]
                否则, 为:  [cpu核数,内存大小, 0]
        T:  共有T天的用户请求序列, list
        requests:  所有的用户请求序列, list
            [   [[第一天第一条请求], [第一天第二条请求], ...],
                [[第二天第一条请求], [第二天第二条请求], ...],
                ...     ...
            ]
    '''
    # 需要提交时把下三行代码注释即可
    import sys
    filename = "./training-data/training-1.txt"
    # 将python标准输入input函数重定向为filename
    sys.stdin = open(filename, 'r')

    # 可以采购的服务器类型数量
    N = int(input())
    # 总服务器类型
    servers = {}
    # 遍历每种服务器
    for i in range(N):
        server = []
        infomations_server = extract(input())
        # 服务器型号
        type = infomations_server[0].strip()
        # cpu核数
        cpu = int(infomations_server[1].strip())
        server.append(cpu)
        # 内存大小
        memory = int(infomations_server[2].strip())
        server.append(memory)
        # 硬件成本
        cost_hardware = int(infomations_server[3].strip())
        server.append(cost_hardware)
        # 每日能耗成本
        cost_day = int(infomations_server[4].strip())
        server.append(cost_day)
        servers[type] = server

    # 售卖的虚拟机类型数量
    M = int(input())
    virtualMachines = {}
    # 遍历每种虚拟机类型
    for i in range(M):
        vm = []
        infomations_vm = extract(input())
        type = infomations_vm[0].strip()
        cpu = int(infomations_vm[1].strip())
        memory = int(infomations_vm[2].strip())
        isTwoNode = int(infomations_vm[3].strip())
        # 若虚拟机是双节点
        if isTwoNode == 1:
            vm.append(cpu/2)
            vm.append(memory/2)
            vm.append(isTwoNode)
            vm.append(cpu / 2)
            vm.append(memory / 2)
        else:
            vm.append(cpu)
            vm.append(memory)
            vm.append(isTwoNode)
        virtualMachines[type] = vm
    # T天的用户请求
    T = int(input())
    requests = []
    for i in range(T):
        # 第i天的R条请求
        R = int(input())
        # 一天的请求
        requests_day = []
        # 第i天的第j条请求
        for j in range(R):
            request = []
            req = extract(input())
            opration = req[0].strip()
            request.append(opration)
            if opration=="add":
                type = req[1].strip()
                request.append(type)
                id = int(req[2].strip())
                request.append(id)
            else:
                id = int(req[1].strip())
                request.append(id)
            requests_day.append(request)
        requests.append(requests_day)
    # 返回服务器类型数量，每种服务器信息，每种虚拟机信息，总天数，总请求信息
    return N, servers, M, virtualMachines, T, requests
