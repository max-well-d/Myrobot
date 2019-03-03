import time, sched, os
from threading import Timer

# 初始化sched模块的scheduler类 
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。 
'''
schedule = sched.scheduler(time.time, time.sleep) 
  
def pit():
    print ("fit")
# 被周期性调度触发的函数 
def execute_command(inc): 
    times = time.time()
    times = time.strftime("%H:%M",time.localtime(times))
    print(times)
    pit()
    schedule.enter(inc, 0, execute_command, (inc,)) 
# 每60秒查看下网络连接情况 
if __name__ == '__main__': 
    inc = 60
    schedule.enter(0, 0, execute_command, (inc,)) 
    schedule.run()
    print("finish")
'''

def another_command():
    print ("ok")
# 被周期性调度触发的函数 
def execute_command(inc): 
    times = time.time()
    times = time.strftime("%H:%M",time.localtime(times))
    print(times)
    next_ = Timer(10, execute_command,(10,))
    next_.start()
#能输出
    Timer(11, another_command).start()
    return "ojbk"
if __name__ == '__main__': 
    inc = 10
    a = execute_command(inc)
    print(a)