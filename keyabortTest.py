# coding=utf-8
# Aug 13, 2018 11:52
# author:jevde
import time
import datetime

str1 = '+hello world\r\n12313'

# print(str1.split('\r\n'))
# print('stime:', datetime.datetime.now())
# try:
#     while True:
#         time.sleep(1)
#         print('go')
# except KeyboardInterrupt:
#     print('键盘中断')
#     print('etime:', datetime.datetime.now())
# finally:
#     print('完成')
class RedisProtocol():
    ONE_LINE_ARROW = '+'
    MUL_LINE_ARROW = '$'
    INT_ARROW = ':'
    ERROE_ARROW = '-'
    ARRAY_ARROW = '*'
    def text_decode(self,text):
        value = None
        return value
    def value_encode(self,value):
        text = None
        return text


ONE_LINE_ARROW = '+'
MUL_LINE_ARROW = '$'
INT_ARROW = ':'
ERROE_ARROW = '-'
ARRAY_ARROW = '*'
str1 = '+hello world\r\n$11\r\n12313 12344\r\n:2344\r\n-WRONGTYPE Operation against a key holding the wrong kind of value\r\n*3\r\n:1:3:5'

handles = {
    ONE_LINE_ARROW :process_single_line,
    MUL_LINE_ARROW :process_mul_line,
    INT_ARROW :process_number,
    ERROE_ARROW :process_warning,
    ARRAY_ARROW :process_array,
}


def process_single_line(value_list,line,index):
    step = 1
    return line.split(ONE_LINE_ARROW)[-1], step

def process_mul_line(value_list,line,index):
    length = int(str1.split(MUL_LINE_ARROW)[-1])
    step = 2
    if length!=len(value_list[index+1]):
        raise Exception
    return value_list[index+1],step

def process_number(value_list,line,index):
    step = 1
    return int(line.split(INT_ARROW)[-1]),step

def process_warning(value_list,line,index):
    step = 1
    return int(line.split(ERROE_ARROW)[-1]),step

def process_array(value_list,line,index):
    step = 1
    values = []
    length = int(str1.split(ARRAY_ARROW)[-1])
    while length>0:
        value,the_step = handles[value_list[index][0]](value_list,value_list[index],index)
        values.append(value)
        length -= 1
        step += the_step
    return values,step

def redis_string(str_redis):
    values = []
    value_list = str_redis[:-2].split('\r\n')
    index = 0
    while index< len(value_list):
        value,step = handles[value_list[index][0]](value_list,value_list[index],index)
        index += step
        values.append(value)
    return values
print(redis_string('+hello world\r\n$11\r\n12313 12344\r\n*3\r\n:3\r\n:3\r\n:3\r\n'))


ste = '$-1\r\n$0\r\n'
ss=ste.split('\r\n')
print(ss)


