import time

import get_data
from cal_cost import cal_cost

servers_Num, servers_Dict, vm_Num, vm_Dict, Days, req_Sqe = get_data.get_input()
vm_perfom = []
servers_perfom = []

def vm_statist():
	'''
	统计虚拟机类型cpu内存比
	'''
	for vm_inf in vm_Dict.values():
		# print(vm_inf)
		vm_perfom.append(vm_inf[0]/vm_inf[1])

def servers_statist():
	'''
	统计服务器cpu内存
	'''
	for type, servers_inf in servers_Dict.items():
		# print(servers_inf)
		servers_perfom.append([servers_inf[0]/servers_inf[1], servers_inf[2], type])

def servers_Pcha():
	'''
	返回服务器类型
	'''
	best = 0
	for type, servers_inf in servers_Dict.items():
		# print(servers_inf)
		score = (servers_inf[0]*servers_inf[1])/servers_inf[2]
		if best < score:
			best = score
			B_type = type
	return B_type


def vm_Migra():
	pass


def vm_add():
	pass


def vm_del():
	pass


def main():
	'''
	需求驱动，单步策略，不进行迁移
	'''
	# vm_statist()
	# servers_statist()
	servers_Pool = []  # 现有服务器集群[[type,cup_A,menmery_A,cup_B,menmery_B,open_or_close],...]#后期可以对象化，全局的吧,加一个虚拟机列表加快查找
	vm_Pool = {}  # 现有虚拟机列表{vm_id:[servers_id,cup_A,menmery_A,cup_B,menmery_B]}#后面记录的是该虚拟机的cpu和内存

	costSum = 0  # 总费用

	for j in range(Days):
		purchase = 0
		purchase_dict = {}  # 购买的服务器列表{servers_type:num,...}
		migration = 0
		migration_list = []  # 迁移的服务器列表[[vm_id,servers_id,node],...]
		scheme = []  # [[servers_id,node],...]
		for request in req_Sqe[j]:
			process = 0  # 表示未处理,如果一天的请求就是[0 for in range[len(req_sqe[i])]]，后期可以弄个多天的
			while process == 0:  # 只有process完才能结束
				if request[0] == 'add':  # 部署
					if vm_Dict[request[1]][2] == 0:  # 单节点部署
						for i in range(len(servers_Pool)):  # 遍历现有服务器集群，第一个可以的部署
							if servers_Pool[i][1] > vm_Dict[request[1]][0] and servers_Pool[i][2] > vm_Dict[request[1]][1]:  # 找到服务器
								# print(servers_Pool,request,vm_Pool)
								servers_Pool[i][1] -= vm_Dict[request[1]][0]  # 资源分配
								servers_Pool[i][2] -= vm_Dict[request[1]][1]
								scheme.append([i, 'A'])
								vm_Pool[request[2]] = [i, *vm_Dict[request[1]][0:2], 0, 0]  # 加入虚拟机列表
								# print(servers_Pool)
								process = 1
								break
							elif servers_Pool[i][3] > vm_Dict[request[1]][0] and servers_Pool[i][4] > vm_Dict[request[1]][1]:
								servers_Pool[i][3] -= vm_Dict[request[1]][0]  # 资源分配
								servers_Pool[i][4] -= vm_Dict[request[1]][1]
								scheme.append([i, 'B'])
								vm_Pool[request[2]] = [i, 0, 0, *vm_Dict[request[1]][0:2]]  # 加入虚拟机列表
								process = 1
								break
					elif vm_Dict[request[1]][2] == 1:  # 双节点部署
						for i in range(len(servers_Pool)):  # 这个循环可以跟上面那个合并
							vm_need = [vm_Dict[request[1]][0]/2, vm_Dict[request[1]][1]/2]
							if servers_Pool[i][1] > vm_need[0] and servers_Pool[i][3] > vm_need[0] \
									and servers_Pool[i][2] > vm_need[1] and servers_Pool[i][4] > vm_need[1]:
								servers_Pool[i][1] -= vm_need[0]  # 资源分配
								servers_Pool[i][2] -= vm_need[1]
								servers_Pool[i][3] -= vm_need[0]
								servers_Pool[i][4] -= vm_need[1]
								scheme.append([i])
								vm_Pool[request[2]] = [i, *vm_need, *vm_need]  # 加入虚拟机列表
								process = 1
								break
				elif request[0] == 'del':  # 删除
					servers_id = vm_Pool[request[1]][0]
					servers_Pool[servers_id][1] += vm_Pool[request[1]][1]
					servers_Pool[servers_id][2] += vm_Pool[request[1]][2]
					servers_Pool[servers_id][3] += vm_Pool[request[1]][3]
					servers_Pool[servers_id][4] += vm_Pool[request[1]][4]  # 释放资源 CPU、内存
					process = 1  # 需求已处理
					# servers_type=servers_Pool[servers_id][0]
					# if serpool_Dict[servers_type][0:2]==servers_Pool[servers_id][1:2:2]+servers_Pool[servers_id][2:2:2]:  # 服务器没有虚拟机运行，计算成本的时候才需要
					del vm_Pool[request[1]]
				if process == 0:
					servers_type = servers_Pcha()  # 确定服务器购买类型,后期可返回待选服务器类型
					if servers_type in purchase_dict:
						purchase_dict[servers_type] += 1
					else:
						purchase_dict[servers_type] = 1
						purchase += 1
					servers_Pool.append([servers_type, servers_Dict[servers_type][0]/2, servers_Dict[servers_type][1]/2, servers_Dict[servers_type][0]/2, servers_Dict[servers_type][1]/2, 1])
		migration_list = vm_Migra()  # 虚拟机迁移，启发式迁移

		print('(purchase, '+str(purchase)+')')  # 输出,后期写成一个函数
		for key, values in purchase_dict.items():
			print('('+str(key)+', '+str(values)+')')
		print('(migration, '+str(migration)+')')
		# for mig in migration_list:
			# if len(mig)==2:
				# sys.stdout.write('('+str(mig[0])+','+str(mig[1])+')\n')
			# if len(mig)==3:
				# sys.stdout.write('('+str(mig[0])+','+str(mig[1])+','+str(mig[2])+')\n')
		for sch in scheme:
			if len(sch) == 1:
				print('('+str(sch[0])+')')
			if len(sch) == 2:
				print('('+str(sch[0])+', '+str(sch[1])+')')

		costSum += cal_cost(purchase_dict, servers_Pool)

	print("costSum总成本:", costSum)


if __name__=='__main__':
	start = time.process_time()
	main()
	end = time.process_time()

	print("运行时间：", end - start)
