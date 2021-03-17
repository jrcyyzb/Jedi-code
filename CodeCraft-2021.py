import time

import get_data
# import numpy as np
from cal_cost import cal_cost

# 使用 最便宜的 服务器

# 返回的虚拟机和服务器表可以处理一下，双节点的就按双节点的存
servers_Num, servers_Dict, vm_Num, vm_Dict, Days, req_Sqe = get_data.get_input()
vm_perfom = []
# 所有服务器统计信息，格式为[[型号, 硬件成本], ...]
servers_perfom = []


def choose_server(request):
    '''
    服务器放不下请求所需的虚拟机时，选择一种服务器
    request 是一个add请求
    :param request:
    :return:
    '''
    vm_type = request[1]
    vm_cpu = vm_Dict[vm_type][0]
    vm_memory = vm_Dict[vm_type][1]
    vm_node = vm_Dict[vm_type][2]   # 是否双节点部署
    for servers in servers_perfom:
        server_type = servers[0]
        server_cpu = servers_Dict[server_type][0] / 2
        server_memory = servers_Dict[server_type][1] / 2
        if vm_cpu <= server_cpu and vm_memory <= server_memory:
            return server_type



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


# 统计服务器硬件信息
def servers_statist():
    '''
    统计服务器cpu内存比
    '''
    for type, servers_inf in servers_Dict.items():
        # print(servers_inf)
        servers_perfom.append([type, servers_inf[2]])


def vm_Migra(servers_pool, ):  # 有可能就往一台机子上移，大的先移
    pass


class days_ans:
    '''
    可选天数的安排类
    '''

    def __init__(self):
        self.purchase = 0   # 记录买的服务器类型数
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

    def Buy_server(self, servers_type):  # 买入服务器
        self.servers_pool.append([servers_type, servers_Dict[servers_type][0] / 2,
                              servers_Dict[servers_type][1] / 2, servers_Dict[servers_type][0] / 2,
                              servers_Dict[servers_type][1] / 2, 1])

    def Del(self, id, vm_inf):  # 删除虚拟机
        self.servers_pool[id][1] += vm_inf[0]
        self.servers_pool[id][2] += vm_inf[1]
        self.servers_pool[id][3] += vm_inf[2]
        self.servers_pool[id][4] += vm_inf[3]  # 释放资源

    def reserch(self, vm_inf):  # 返回可行的服务器id列表

        return id


# 现有服务器集群[[type,cup_A,menmery_A,cup_B,menmery_B,{runing_vm_list}],...]#加一个虚拟机列表加快查找,后期迁移优化
servers_Pool = servers_POOL()



def main():
    vm_Pool = {}  # 现有虚拟机列表{vm_id:[servers_id,cup_A,menmery_A,cup_B,menmery_B,del_days]}#后面记录的是该虚拟机的cpu和内存,最后一个是虚拟机要被删除的时间
    costSum = 0  # 总费用

    servers_statist()   # 统计服务器硬件成本
    # 根据硬件成本从小到大排序
    servers_perfom.sort(key=lambda servers_perfom: servers_perfom[1])

    '''
    需求驱动，单步策略，不进行迁移
    '''
    for j in range(Days):
        answer_1d = days_ans()
        for request in req_Sqe[j]:
            process = 0  # 表示未处理,如果一天的请求就是[0 for in range[len(req_sqe[i])]]，后期可以弄个多天的
            if request[0] == 'add':  # 部署
                if vm_Dict[request[1]][2] == 0:  # 单节点部署
                    for i in range(len(servers_Pool)):  # 遍历现有服务器集群，第一个可以的部署
                        if servers_Pool.Add_vm(i, [*vm_Dict[request[1]][0:2], 0, 0]):  # 如果可以加
                            answer_1d.scheme.append([str(i), 'A'])
                            vm_Pool[request[2]] = [i, *vm_Dict[request[1]][0:2], 0, 0]  # 加入虚拟机列表
                            process = 1
                            break
                        elif servers_Pool.Add_vm(i, [0, 0, *vm_Dict[request[1]][0:2]]):
                            answer_1d.scheme.append([str(i), 'B'])
                            vm_Pool[request[2]] = [i, 0, 0, *vm_Dict[request[1]][0:2]]  # 加入虚拟机列表
                            process = 1
                            break
                    # 若不能加
                    if process == 0:
                        # 则购买服务器，默认先放入A节点
                        server_type = choose_server(request)
                        servers_Pool.Buy_server(server_type)
                        if server_type in answer_1d.purchase_dict:
                            answer_1d.purchase_dict[server_type] += 1
                        else:
                            answer_1d.purchase_dict[server_type] = 1
                            answer_1d.purchase += 1
                        id = len(servers_Pool) - 1  # 新购买的服务器id
                        servers_Pool.Add_vm(id, [*vm_Dict[request[1]][0:2], 0, 0])
                        answer_1d.scheme.append([str(id), 'A'])
                        vm_Pool[request[2]] = [id, *vm_Dict[request[1]][0:2],0, 0]  # 加入虚拟机列表
                elif vm_Dict[request[1]][2] == 1:  # 双节点部署
                    for i in range(len(servers_Pool)):  # 这个循环可以跟上面那个合并
                        # vm_need=[vm_Dict[request[1]][0]/2,vm_Dict[request[1]][1]/2]
                        if servers_Pool.Add_vm(i, [*vm_Dict[request[1]][0:2], *vm_Dict[request[1]][0:2]]):
                            answer_1d.scheme.append([str(i)])
                            vm_Pool[request[2]] = [i, *vm_Dict[request[1]][0:2],*vm_Dict[request[1]][0:2]]  # 加入虚拟机列表
                            process = 1
                            break
                    if process == 0:
                        server_type = choose_server(request)
                        servers_Pool.Buy_server(server_type)
                        if server_type in answer_1d.purchase_dict:
                            answer_1d.purchase_dict[server_type] += 1
                        else:
                            answer_1d.purchase_dict[server_type] = 1
                            answer_1d.purchase += 1
                        id = len(servers_Pool) - 1  # 新买的服务器id
                        servers_Pool.Add_vm(id, [*vm_Dict[request[1]][0:2], *vm_Dict[request[1]][0:2]])
                        answer_1d.scheme.append([str(id)])
                        vm_Pool[request[2]] = [id, *vm_Dict[request[1]][0:2], *vm_Dict[request[1]][0:2]]
            elif request[0] == 'del':  # 删除
                servers_id = vm_Pool[request[1]][0]
                # print(vm_Pool[request[1]][1:5])
                servers_Pool.Del(servers_id, vm_Pool[request[1]][1:5])
                process = 1  # 需求已处理
                del vm_Pool[request[1]]

        # answer_1d.migration_list = vm_Migra()  # 虚拟机迁移，启发式迁移
        costSum += cal_cost(answer_1d.purchase_dict, servers_Pool.servers_pool)
        answer_1d.output()  # 打印输出

    print("costSum总成本:", costSum)


if __name__ == '__main__':
    start = time.process_time()
    main()
    end = time.process_time()
    print("运行时间：", end - start)
