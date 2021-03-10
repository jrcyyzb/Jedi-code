# -*- coding: utf-8 -*-
# @Author: Hugh
# @Date: 2021/3/10 17:52
# Software: PyCharm
# 获取数据集中的数据


# 将服务器/虚拟机数据格式转化为列表
def extract(detail):
    infomation = detail.rstrip("\n")
    infomation = infomation[1:len(infomation)-1]
    return infomation.split(",")


def get_input(filename, data_path="./training-data"):
    '''
    提取filename数据集中的输入
    :param filename: 数据集名称
    :param data_path: 数据集所在文件夹路径
    :return:
        N:  可以采购的服务器类型数量, int
        servers:  所有服务器类型信息, dict.
            {'第一种服务器类型型号':[cpu核数,内存大小,硬件成本,每日能耗成本], '第二种...':..., ...}
        M:  售卖的虚拟机类型数量, int
        virtualMachines:  所有虚拟机类型信息, dict
            {'第一种虚拟机型号':[cpu核数,内存大小,是否双节点部署], '第二种...':...}
        T:  共有T天的用户请求序列, list
        requests:  所有的用户请求序列, list
            [   [[第一天第一条请求], [第一天第二条请求], ...],
                [[第二天第一条请求], [第二天第二条请求], ...],
                ...     ...
            ]
    '''
    with open(data_path + "/" + filename, "r") as f:
        details = f.readlines()
    # 可以采购的服务器类型数量
    N = int(details[0].rstrip("\n"))
    # 总服务器类型
    servers = {}
    # 遍历每种服务器
    for i in range(1, N + 1):
        server = []
        infomations_server = extract(details[i])
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
    M = int(details[N + 1].rstrip("\n"))
    virtualMachines = {}
    # 遍历每种虚拟机类型
    for i in range(N + 2, N + M + 2):
        vm = []
        infomations_vm = extract(details[i])
        type = infomations_vm[0].strip()
        cpu = int(infomations_vm[1].strip())
        vm.append(cpu)
        memory = int(infomations_vm[2].strip())
        vm.append(memory)
        isTwoNode = int(infomations_vm[3].strip())
        vm.append(isTwoNode)
        virtualMachines[type] = vm
    # T天的用户请求
    T = int(details[N + M + 2].rstrip("\n"))
    requests = []
    idx = N + M + 3
    for i in range(T):
        # 第i天的R条请求
        R = int(details[idx].rstrip("\n"))
        # 一天的请求
        requests_day = []
        # 第i天的第j条请求
        for j in range(R):
            request = []
            req = extract(details[idx+j+1])
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
        idx += R + 1
        requests.append(requests_day)
    # 返回服务器类型数量，每种服务器信息，每种虚拟机信息，总天数，总请求信息
    return N, servers, M, virtualMachines, T, requests
