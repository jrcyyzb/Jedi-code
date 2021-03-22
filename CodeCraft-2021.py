# -*- coding: utf-8 -*-
# @Author: Hugh
# @Date: 2021/3/20 13:14
# Software: PyCharm

from Solver import *

# import time


def main():
    ioUtil = IOUtil()
    # N 服务器类型数
    N = ioUtil.readServerTypes()
    # M 虚拟机类型数
    M = ioUtil.readVirtualHosts()
    # 总天数
    T = readInt()
    solver = Solver(ioUtil, T)

    for i in range(T):

        # if i % 100 == 0:
        #     print("process day", i)

        # 第i天请求数
        R = solver.ioUtil.readRequests()
        solver.dailyRoutine(i)

    for s in solver.ioUtil.outputs:
        print(s)

    # solver.displayCost()

if __name__ == "__main__":
    # start = time.process_time()
    main()
    # end = time.process_time()
    # print("运行时间：", end-start)