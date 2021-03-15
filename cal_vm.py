import get_data

servers_Num, servers_Dict, vm_Num, vm_Dict, Days, req_Sqe = get_data.get_input()

vm_Pool = {}  # 现有虚拟机列表{vm_id:[fisrtday]}#后面记录的是该虚拟机的cpu和内存


if __name__=='__main__':
    for j in range(Days):
        scheme = []  # [[servers_id,node],...]
        for request in req_Sqe[j]:
            if request[0] == 'add':
                vm_Pool[request[2]] = [j]  # 加入虚拟机列表
                print("id: ", request[2], " day: ", j)
            elif request[0] == 'del':  # 删除
                print("id:", request[1], "天数：", j-vm_Pool[request[1]][0])