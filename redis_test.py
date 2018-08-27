# -*- coding:utf-8 -*-
__author__ = 'Jevade'
__data__ = '2018/8/6 21:29'
import redis

def singleton(cls):
    instance = {}
    def _singleton(*args, **kw):
        if cls not in instance:
            instance[cls] = cls(*args,**kw)
        return instance[cls]
    return _singleton

@singleton
class RedisPool():
    '''提供Redis连接池'''
    host = 'localhost'
    port = 6379
    pool = None
    conn = None
    def __init__(self,host=host,port=port):
        self.pool = redis.ConnectionPool(host=host,port=port,decode_responses=True)
    
    def __enter__(self):
        return self.get_connect()
    
    def get_connect(self):
        '''获取Redis链接'''
        return redis.Redis(connection_pool=self.pool)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Templist(object):
    def __enter__(self):
        print("enter the class instance")
        return self
    def do_something(self):
        print('I am doing some things.')
        print(1//0)
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("type: ", exc_type)
        print("val: ", exc_val)
        print("tb: ", exc_tb) 



if __name__=="__main__":
    with  RedisPool() as redis_conn:
        redis_conn.delete('liu')
        redis_conn.set('liu', 'jiawei')
        redis_conn.set('c', 123)
        redis_conn.set('array', [12,34,56,77],)
        print(redis_conn.get('liu'))
        redis_pool2 = RedisPool()
        redis_conn.hset(name="info",key='c', value=123)
        print(redis_conn.hgetall(name="info"))

    with Templist() as templist:
        templist.do_something()

