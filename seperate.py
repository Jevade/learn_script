
import random, time, queue
from multiprocessing.managers import BaseManager

put_queue=queue.Queue()
get_queue=queue.Queue()

class managerClass(BaseManager):
	pass
managerClass.register("put_task_queue",callable=lambda:put_queue)
managerClass.register("get_task_queue",callable=lambda:get_queue)
managers=managerClass(address=('',5000),authkey=b'abc')
managers.start()

task=managers.put_task_queue()
result=managers.get_task_queue()

for i in range(100):
    n = random.randint(0, 10000)
    print('Put task %d...' % n)
    task.put(n)
print("put task")

print('Try get results...')
for i in range(10):
    r = result.get(True)
    print('Result: %s' % r)
# 关闭:
manager.shutdown()
print('master exit.')
