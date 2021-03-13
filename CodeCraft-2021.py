import time

import get_data
from cal_cost import cal_cost

servers_Num, servers_Dict, vm_Num, vm_Dict, Days, req_Sqe=get_data.get_input()#返回的虚拟机和服务器表可以处理一下，双节点的就按双节点的存
vm_perfom=[]
servers_perfom=[]

def request_statist():
	'''
	统计虚拟机几天后运行信息
	'''
	pass

def vm_statist():
	'''
	统计虚拟机类型cpu内存比，统计虚拟机运行时间
	'''
	for vm_inf in vm_Dict.values():
		#print(vm_inf)
		vm_perfom.append(vm_inf[0]/vm_inf[1])
	pass

def servers_statist():
	'''
	统计服务器cpu内存
	'''
	for type,servers_inf in servers_Dict.items():
		#print(servers_inf)
		servers_perfom.append([servers_inf[0]/servers_inf[1],servers_inf[2],type])
	pass

def servers_Pcha(futrdy_reqst):#优化重点,
	'''
	根据未来需求，返回服务器类型字典{type:num}
	'''
	best=0;
	for type,servers_inf in servers_Dict.items():
		#print(servers_inf)
		score=(servers_inf[0]*servers_inf[1])/servers_inf[2]#/servers_inf[3]
		if best<score:
			best=score
			B_type=type
	#print(B_type)
	return B_type

def vm_Migra(servers_pool,):#有可能就往一台机子上移，大的先移
	pass

class days_ans:
	'''
	可选天数的安排类
	'''
	def __init__(self):
		self.purchase=0
		self.purchase_dict={}#{servers_type:num,...}
		self.migration=0
		self.migration_list=[]#[[vm_id,servers_id,node],...]
		self.scheme=[]
	def output(self):
		print('(purchase, '+str(self.purchase)+')')  # 输出,后期写成一个函数
		for key, values in self.purchase_dict.items():
			print('('+str(key)+', '+str(values)+')')
		print('(migration, '+str(self.migration)+')')
		# for mig in self.migration_list:
			# if len(mig)==2:
				# print('('+str(mig[0])+','+str(mig[1])+')\n')
			# if len(mig)==3:
				# print('('+str(mig[0])+','+str(mig[1])+','+str(mig[2])+')\n')
		for sch in self.scheme:
			if len(sch) == 1:
				print('('+str(sch[0])+')')
			if len(sch) == 2:
				print('('+str(sch[0])+', '+str(sch[1])+')')


class servers_POOL:
	'''
	服务器集群类
	'''
	def __init__(self):
		self.servers_pool=[]
	def __len__(self):
		return len(self.servers_pool)
	def Add_vm(self,id,vm_inf):  # 如果可以加就加，不能加会返回false
		if self.servers_pool[id][1]<vm_inf[0] or\
			self.servers_pool[id][2]<vm_inf[1] or\
			self.servers_pool[id][3]<vm_inf[2] or\
			self.servers_pool[id][4]<vm_inf[3] : return False
		self.servers_pool[id][1]-=vm_inf[0]  # 分配资源
		self.servers_pool[id][2]-=vm_inf[1]
		self.servers_pool[id][3]-=vm_inf[2]
		self.servers_pool[id][4]-=vm_inf[3]
		return True
	def Buy_server(self,servers_type):#买入服务器
		self.servers_pool.append([servers_type,servers_Dict[servers_type][0]/2,\
		servers_Dict[servers_type][1]/2,servers_Dict[servers_type][0]/2,servers_Dict[servers_type][1]/2,1])
	def Del(self,id,vm_inf):#删除虚拟机
		self.servers_pool[id][1]+=vm_inf[0]
		self.servers_pool[id][2]+=vm_inf[1]
		self.servers_pool[id][3]+=vm_inf[2]
		self.servers_pool[id][4]+=vm_inf[3]#释放资源
	def reserch(self,vm_inf):#返回可行的服务器id列表
		
		return id


def main():
	'''
	需求驱动，单步策略，不进行迁移
	'''

	servers_Pool=servers_POOL()  # 现有服务器集群[[type,cup_A,menmery_A,cup_B,menmery_B,{runing_vm_list}],...]#加一个虚拟机列表加快查找,后期迁移优化
	vm_Pool={}  # 现有虚拟机列表{vm_id:[servers_id,cup_A,menmery_A,cup_B,menmery_B,del_days]}#后面记录的是该虚拟机的cpu和内存,最后一个是虚拟机要被删除的时间
	costSum = 0  # 总费用

	for j in range(Days):
		answer_1d=days_ans()
		servers_type=servers_Pcha(req_Sqe[j])  # 确定服务器购买类型,后期可返回待选服务器类型,可以先买几台服务器，不够再加
		for request in req_Sqe[j]:
			process=0#表示未处理,如果一天的请求就是[0 for in range[len(req_sqe[i])]]，后期可以弄个多天的
			while process==0:#只有process完才能结束
				#print(len(servers_Pool))
				if request[0]=='add':#部署
					if vm_Dict[request[1]][2]==0:#单节点部署
						for i in range(len(servers_Pool)):#遍历现有服务器集群，第一个可以的部署 
							#print(servers_Pool.servers_pool[i])
							if servers_Pool.Add_vm(i,[*vm_Dict[request[1]][0:2],0,0]):#如果可以加
								answer_1d.scheme.append([str(i),'A'])
								vm_Pool[request[2]]=[i,*vm_Dict[request[1]][0:2],0,0]#加入虚拟机列表
								process=1
								break
							elif servers_Pool.Add_vm(i,[0,0,*vm_Dict[request[1]][0:2]]):
								answer_1d.scheme.append([str(i),'B'])
								vm_Pool[request[2]]=[i,0,0,*vm_Dict[request[1]][0:2]]#加入虚拟机列表
								process=1
								break
					elif vm_Dict[request[1]][2]==1:#双节点部署
						for i in range(len(servers_Pool)):#这个循环可以跟上面那个合并
							#vm_need=[vm_Dict[request[1]][0]/2,vm_Dict[request[1]][1]/2]
							if servers_Pool.Add_vm(i,[*vm_Dict[request[1]][0],*vm_Dict[request[1]][0]]):
								answer_1d.scheme.append([str(i)])
								vm_Pool[request[2]]=[i,*vm_need,*vm_need]#加入虚拟机列表
								process=1
								break
				elif request[0]=='del':#删除
					servers_id=vm_Pool[request[1]][0]
					#print(vm_Pool[request[1]][1:5])
					servers_Pool.Del(servers_id,vm_Pool[request[1]][1:5])
					process=1#需求已处理
					del vm_Pool[request[1]]
				if process==0:
					#print(answer_1d.purchase)
					servers_type=servers_Pcha(request)
					if servers_type in answer_1d.purchase_dict:
						answer_1d.purchase_dict[servers_type]+=1
					else:
						answer_1d.purchase_dict[servers_type]=1
						answer_1d.purchase+=1
					servers_Pool.Buy_server(servers_type)
		answer_1d.migration_list=vm_Migra()#虚拟机迁移，启发式迁移
		costSum += cal_cost(answer_1d.purchase_dict, servers_Pool.servers_pool)
		answer_1d.output()#打印输出
	print("costSum总成本:", costSum)

if __name__=='__main__':
	start = time.process_time()
	main()
	end = time.process_time()

	print("运行时间：", end - start)