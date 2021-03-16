import time

import get_data
import numpy as np
from cal_cost import cal_cost

# 返回的虚拟机和服务器表可以处理一下，双节点的就按双节点的存
servers_Num, servers_Dict, vm_Num, vm_Dict, Days, req_Sqe = get_data.get_input()
vm_perfom = []
# 所有服务器统计信息，格式为[[型号, cpu/内存, 硬件成本], ...]
servers_perfom = []


def servers_fit_vm(max_vm_type, left, right):
    '''
    在下标为[left, right)范围的服务器内选取能容纳max_vm_type的服务器型号
    :return  返回满足条件的服务器型号
    '''
    for i in range(left, right):
        servers_type = servers_perfom[i][0]
        cpu = servers_Dict[servers_type][0] / 2
        memory = servers_Dict[servers_type][1] / 2
        # cpu最大的虚拟机型号
        vmCpu_type = max_vm_type[0]
        # 内存最大的虚拟机型号
        vmMemory_type = max_vm_type[1]
        # 若服务器资源容纳不下最大虚拟机
        if vm_Dict[vmCpu_type][0] > cpu or vm_Dict[vmMemory_type][0] > cpu \
                or vm_Dict[vmCpu_type][1] > memory or vm_Dict[vmMemory_type][1] > memory:
            continue
        return servers_type


# 选出三类服务器
def choose_servers(max_vm_types):
    '''
    选出三类服务器, 其中每类服务器的cpu/内存资源必须不小于虚拟机最大资源
    :max_vm_types  每类cpu/内存资源最大的虚拟机型号, list
        [[第一类最大cpu虚拟机型号, 第一类最大内存虚拟机型号], [...], [...]]
    '''
    # 统计服务器 cpu 内存比
    servers_statist()
    # 根据cpu/内存比从小到大排序
    servers_perfom.sort(key=lambda server: server[1])
    # 选取小型服务器
    S = servers_fit_vm(max_vm_types[2], int(servers_Num * 0.3), int(servers_Num * 0.6))
    M = servers_fit_vm(max_vm_types[1], int(servers_Num * 0.6), int(servers_Num * 0.9))
    L = servers_fit_vm(max_vm_types[0], int(servers_Num * 0.9), servers_Num)

    # 返回三种类型服务器型号
    return L, M, S


# 划分三类虚拟机
def split_vm():
    '''
    划分三类虚拟机
    :return
        vm_L, cpu/内存比大的虚拟机型号
        vm_M, cpu/内存比中的虚拟机型号
        vm_S: cpu/内存比小的虚拟机型号
        max_types: 三类虚拟机中cpu最大、内存最大的虚拟机。只用于选择符合条件的服务器
    '''
    # 选出三种类型的虚拟机以对应三种服务器
    types = list(vm_Dict.keys())  # 返回虚拟机所有型号列表
    vm_L = types[:int(vm_Num * 0.3)]  # cpu/内存 大
    vm_M = types[int(vm_Num * 0.3):int(vm_Num * 0.6)]
    vm_S = types[int(vm_Num * 0.6):]  # cpu/内存 小

    # 分别在三种类型的虚拟机中选出最大cpu和最大内存的虚拟机
    vm_infs = list(vm_Dict.values())  # 返回虚拟机所有型号的其他信息列表

    # 将vm_infs信息分成三类，对应三类虚拟机信息
    infs_one = vm_infs[:int(vm_Num * 0.3)]
    infs_two = vm_infs[int(vm_Num * 0.3):int(vm_Num * 0.6)]
    infs_three = vm_infs[int(vm_Num * 0.6):]

    # 转化成numpy数组，利用np.argmax()求得符合条件的虚拟机型号
    one_np = np.array(infs_one)
    two_np = np.array(infs_two)
    three_np = np.array(infs_three)

    # 取出cpu最大和内存最大的虚拟机索引
    one_idx = list(np.argmax(one_np, axis=0)[:2])  # one_idx格式：[cpu最大的虚拟机索引，内存最大的虚拟机索引]
    two_idx = list(np.argmax(two_np, axis=0)[:2])
    three_idx = list(np.argmax(three_np, axis=0)[:2])

    # 通过索引找到对应虚拟机型号
    max_types = []
    max_types.append([vm_L[one_idx[0]], vm_L[one_idx[1]]])
    max_types.append([vm_M[two_idx[0]], vm_M[two_idx[1]]])
    max_types.append([vm_S[three_idx[0]], vm_S[three_idx[1]]])

    return vm_L, vm_M, vm_S, max_types


# 计算n天所需的大中小服务器的数量
def nDay_servers(req_Sqe, vm_L, vm_M, vm_S, server_L, server_M, server_S):
    '''
    计算n天所需的大中小服务器的数量
    :req_Sqe  n天里的请求
    '''

    # 三种类型的服务器资源
    cpu_L = servers_Dict[server_L][0]
    memory_L = servers_Dict[server_L][1]
    cpu_M = servers_Dict[server_M][0]
    memory_M = servers_Dict[server_M][1]
    cpu_S = servers_Dict[server_S][0]
    memory_S = servers_Dict[server_S][1]

    cost_L = cost_M = cost_S = [0, 0]
    for day in req_Sqe:
        for request in day:
            if request[0] == 'del':
                continue
            vm_type = request[1]
            cpu_req = vm_Dict[vm_type][0]
            memory_req = vm_Dict[vm_type][1]
            if vm_type in vm_L:  # 若是大服务器，统计所需cpu、内存总成本
                # 若请求是双节点部署
                if vm_Dict[vm_type][2]:
                    cost_L[0] += cpu_req * 2
                    cost_L[1] += memory_req * 2
                else:  # 单节点
                    cost_L[0] += cpu_req
                    cost_L[1] += memory_req
            elif vm_type in vm_M:
                if vm_Dict[vm_type][2]:
                    cost_M[0] += cpu_req * 2
                    cost_M[1] += memory_req * 2
                else:  # 单节点
                    cost_M[0] += cpu_req
                    cost_M[1] += memory_req
            else:
                if vm_Dict[vm_type][2]:
                    cost_S[0] += cpu_req * 2
                    cost_S[1] += memory_req * 2
                else:  # 单节点
                    cost_S[0] += cpu_req
                    cost_S[1] += memory_req
    cpu = round(cost_L[0] / cpu_L + 0.5)
    memory = round(cost_L[1] / memory_L + 0.5)
    num_L = cpu if cpu > memory else memory

    cpu = round(cost_M[0] / cpu_M + 0.5)
    memory = round(cost_M[1] / memory_M + 0.5)
    num_M = cpu if cpu > memory else memory

    cpu = round(cost_S[0] / cpu_S + 0.5)
    memory = round(cost_S[1] / memory_S + 0.5)
    num_S = cpu if cpu > memory else memory

    return num_L, num_M, num_S


# 统计虚拟机几天后运行信息
def request_statist():
    '''
    统计虚拟机几天后运行信息
    '''
    pass


# 统计虚拟机类型cpu内存比，统计虚拟机运行时间
def vm_statist():
    '''
    统计虚拟机类型cpu内存比，统计虚拟机运行时间
    '''
    for vm_inf in vm_Dict.values():
        # print(vm_inf)
        vm_perfom.append(vm_inf[0] / vm_inf[1])
    pass


# 统计服务器 cpu 内存比
def servers_statist():
    '''
    统计服务器cpu内存比
    '''
    for type, servers_inf in servers_Dict.items():
        # print(servers_inf)
        servers_perfom.append([type, servers_inf[0] / servers_inf[1], servers_inf[2]])


def vm_Migra(servers_pool, ):  # 有可能就往一台机子上移，大的先移
    pass


class days_ans:
    '''
    可选天数的安排类
    '''

    def __init__(self):
        self.purchase = 0
        # 记录已买的服务器
        self.purchase_dict = {}  # {servers_type:num,...}
        self.migration = 0
        self.migration_list = []  # [[vm_id,servers_id,node],...]
        # 虚拟机部署的服务器ID,格式为[服务器ID, ... , [服务器ID, 部署节点]]
        self.scheme = []

    def output(self):
        print('(purchase, ' + str(self.purchase) + ')')  # 输出,后期写成一个函数
        for key, values in self.purchase_dict.items():
            print('(' + str(key) + ', ' + str(values) + ')')
        print('(migration, ' + str(self.migration) + ')')
        # for mig in self.migration_list:
        # if len(mig)==2:
        # print('('+str(mig[0])+','+str(mig[1])+')\n')
        # if len(mig)==3:
        # print('('+str(mig[0])+','+str(mig[1])+','+str(mig[2])+')\n')
        for sch in self.scheme:
            if len(sch) == 1:
                print('(' + str(sch[0]) + ')')
            if len(sch) == 2:
                print('(' + str(sch[0]) + ', ' + str(sch[1]) + ')')


class servers_POOL:
    '''
    服务器集群类
    '''

    def __init__(self):
        self.servers_pool = []

    def __len__(self):
        return len(self.servers_pool)

    def Add_vm(self, id, vm_inf):  # 如果可以加就加，不能加会返回false
        if self.servers_pool[id][1] < vm_inf[0] or \
                self.servers_pool[id][2] < vm_inf[1] or \
                self.servers_pool[id][3] < vm_inf[2] or \
                self.servers_pool[id][4] < vm_inf[3]:
            return False
        self.servers_pool[id][1] -= vm_inf[0]  # 分配资源
        self.servers_pool[id][2] -= vm_inf[1]
        self.servers_pool[id][3] -= vm_inf[2]
        self.servers_pool[id][4] -= vm_inf[3]

        return True

    def Buy_server(self, servers_type, size_type):  # 买入服务器
        self.servers_pool.append([servers_type, servers_Dict[servers_type][0] / 2,
                                  servers_Dict[servers_type][1] / 2, servers_Dict[servers_type][0] / 2,
                                  servers_Dict[servers_type][1] / 2, 1, size_type])

    def Del(self, id, vm_inf):  # 删除虚拟机
        self.servers_pool[id][1] += vm_inf[0]
        self.servers_pool[id][2] += vm_inf[1]
        self.servers_pool[id][3] += vm_inf[2]
        self.servers_pool[id][4] += vm_inf[3]  # 释放资源

    def reserch(self, vm_inf):  # 返回可行的服务器id列表

        return id


# 现有服务器集群[[type,cup_A,menmery_A,cup_B,menmery_B,{runing_vm_list}],...]#加一个虚拟机列表加快查找,后期迁移优化
servers_Pool = servers_POOL()
# 划分三类虚拟机
vm_L, vm_M, vm_S, max_vm = split_vm()
# 划分三类服务器
server_L, server_M, server_S = choose_servers(max_vm)


def main():
    vm_Pool = {}  # 现有虚拟机列表{vm_id:[servers_id,cup_A,menmery_A,cup_B,menmery_B,del_days]}#后面记录的是该虚拟机的cpu和内存,最后一个是虚拟机要被删除的时间
    costSum = 0  # 总费用
    '''
    需求驱动，单步策略，不进行迁移
    '''
    # n天计算一次
    n = 10
    s = Days // n  # 整数除法
    # 每n天所需的大中小服务器数量
    for day in range(s):
        # 取n天的请求
        requests = req_Sqe[day * n: (day + 1) * n]
        # 求出requests中所需大中小服务器的数量
        num_L, num_M, num_S = nDay_servers(requests, vm_L, vm_M, vm_S, server_L, server_M, server_S)
        # print("第{}次循环: num_L={}, num_M={}, num_S={}".format(str(i), str(num_L), str(num_M), str(num_S)))

        # 按顺序处理requests
        for j in range(day * n, (day + 1) * n):
            answer_1d = days_ans()
            if j == day*n:
                # 按照类型买服务器，放入池中
                for i in range(num_L):
                    if server_L in answer_1d.purchase_dict:
                        answer_1d.purchase_dict[server_L] += 1
                    else:
                        answer_1d.purchase_dict[server_L] = 1
                        answer_1d.purchase += 1
                    servers_Pool.Buy_server(server_L, 'L')
                for i in range(num_M):
                    if server_M in answer_1d.purchase_dict:
                        answer_1d.purchase_dict[server_M] += 1
                    else:
                        answer_1d.purchase_dict[server_M] = 1
                        answer_1d.purchase += 1
                    servers_Pool.Buy_server(server_M, 'M')
                for i in range(num_S):
                    if server_S in answer_1d.purchase_dict:
                        answer_1d.purchase_dict[server_S] += 1
                    else:
                        answer_1d.purchase_dict[server_S] = 1
                        answer_1d.purchase += 1
                    servers_Pool.Buy_server(server_S, 'S')

            for request in req_Sqe[j]:
                # 判断虚拟机的类型
                vm_model = request[1]
                if vm_model in vm_L:
                    is_type = 'L'
                elif vm_model in vm_M:
                    is_type = 'M'
                else:
                    is_type = 'S'

                process = 0  # 表示未处理,如果一天的请求就是[0 for in range[len(req_sqe[i])]]，后期可以弄个多天的
                while process == 0:  # 只有process完才能结束
                    if request[0] == 'add':  # 部署
                        if vm_Dict[request[1]][2] == 0:  # 单节点部署
                            for i in range(len(servers_Pool)):  # 遍历现有服务器集群，第一个可以的部署
                                if servers_Pool.servers_pool[i][6] == is_type and servers_Pool.Add_vm(i, [*vm_Dict[request[1]][0:2], 0, 0]):  # 如果可以加
                                    answer_1d.scheme.append([str(i), 'A'])
                                    vm_Pool[request[2]] = [i, *vm_Dict[request[1]][0:2], 0, 0]  # 加入虚拟机列表
                                    process = 1
                                    break
                                elif servers_Pool.servers_pool[i][6] == is_type and servers_Pool.Add_vm(i, [0, 0, *vm_Dict[request[1]][0:2]]):
                                    answer_1d.scheme.append([str(i), 'B'])
                                    vm_Pool[request[2]] = [i, 0, 0, *vm_Dict[request[1]][0:2]]  # 加入虚拟机列表
                                    process = 1
                                    break
                        elif vm_Dict[request[1]][2] == 1:  # 双节点部署
                            for i in range(len(servers_Pool)):  # 这个循环可以跟上面那个合并
                                # vm_need=[vm_Dict[request[1]][0]/2,vm_Dict[request[1]][1]/2]
                                if servers_Pool.servers_pool[i][6] == is_type and servers_Pool.Add_vm(i, [*vm_Dict[request[1]][0:2], *vm_Dict[request[1]][0:2]]):
                                    answer_1d.scheme.append([str(i)])
                                    vm_Pool[request[2]] = [i, *vm_Dict[request[1]][0:2],*vm_Dict[request[1]][0:2]]  # 加入虚拟机列表
                                    process = 1
                                    break
                    elif request[0] == 'del':  # 删除
                        servers_id = vm_Pool[request[1]][0]
                        # print(vm_Pool[request[1]][1:5])
                        servers_Pool.Del(servers_id, vm_Pool[request[1]][1:5])
                        process = 1  # 需求已处理
                        del vm_Pool[request[1]]

                    if process == 0:  # 需要根据类型再次购买服务器
                        if is_type == 'L':
                            if server_L in answer_1d.purchase_dict:
                                answer_1d.purchase_dict[server_L] += 1
                            else:
                                answer_1d.purchase_dict[server_L] = 1
                                answer_1d.purchase += 1
                            servers_Pool.Buy_server(server_L, 'L')
                        elif is_type == 'M':
                            if server_M in answer_1d.purchase_dict:
                                answer_1d.purchase_dict[server_M] += 1
                            else:
                                answer_1d.purchase_dict[server_M] = 1
                                answer_1d.purchase += 1
                            servers_Pool.Buy_server(server_M, 'M')
                        else:
                            if server_S in answer_1d.purchase_dict:
                                answer_1d.purchase_dict[server_S] += 1
                            else:
                                answer_1d.purchase_dict[server_S] = 1
                                answer_1d.purchase += 1
                            servers_Pool.Buy_server(server_S, 'S')

            # answer_1d.migration_list = vm_Migra()  # 虚拟机迁移，启发式迁移
            costSum += cal_cost(answer_1d.purchase_dict, servers_Pool.servers_pool)
            answer_1d.output()  # 打印输出

    print("costSum总成本:", costSum)

    # 处理最后不足n天的请求
    if s * n < Days:
        requests = req_Sqe[(s + 1) * n:]
        # 求出requests中所需大中小服务器的数量
        num_L, num_M, num_S = nDay_servers(requests, vm_L, vm_M, vm_S)
        # print("最后一次次循环: num_L={}, num_M={}, num_S={}".format(str(i), str(num_L), str(num_M), str(num_S)))

        # 买服务器，放入池中
        for i in range(num_L):
            servers_Pool.Buy_server(server_L, 'L')
        for i in range(num_M):
            servers_Pool.Buy_server(server_M, 'M')
        for i in range(num_S):
            servers_Pool.Buy_server(server_S, 'S')



if __name__ == '__main__':
    start = time.process_time()
    main()
    end = time.process_time()
    print("运行时间：", end - start)
