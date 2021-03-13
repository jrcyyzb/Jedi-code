import get_data

servers_Num, servers_Dict, vm_Num, vm_Dict, Days, req_Sqe = get_data.get_input()

hardwareSum = 0


def cal_cost(purchase_dict, servers_Pool):

    hardwareSum = 0

    # 硬件成本
    for key, values in purchase_dict.items():
        hardwareSum += servers_Dict[key][2] * values
        # print("硬件成本: ", hardwareSum)

    # 每天能耗成本
    for i in range(len(servers_Pool)):
        name = servers_Pool[i][0]  # 服务器型号
        cpu = servers_Dict[name][0] / 2
        nc = servers_Dict[name][1] / 2
        # print(cpu, nc)
        if servers_Pool[i][1] != cpu or servers_Pool[i][3] != cpu or servers_Pool[i][2] != nc or servers_Pool[i][3] != nc:
            hardwareSum += servers_Dict[name][3]
            # print("每天能耗成本: ", hardwareSum)

    return hardwareSum