import get_data

servers_Num, servers_Dict, vm_Num, vm_Dict, Days, req_Sqe = get_data.get_input()

# hardwareSum = 0


def cal_cost(purchase_dict, servers_Pool):

    hardwareSum = 0

    # 硬件成本
    for key, values in purchase_dict.items():
        hardwareSum += servers_Dict[key][2]
        #print("硬件成本: ", hardwareSum)

    # 每天能耗成本
    for i in range(len(servers_Pool)):
        if servers_Pool[i][1] or servers_Pool[i][2] or servers_Pool[i][3] or servers_Pool[i][4]:
            name = servers_Pool[i][0]  # 服务器型号
            hardwareSum += servers_Dict[name][2]
            #print("每天能耗成本: ", hardwareSum)

    return hardwareSum