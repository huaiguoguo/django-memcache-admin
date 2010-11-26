import socket, StringIO 
import datetime
from django.core.cache import cache


try:
    import memcache
    memcache_installed = True
except ImportError:
    memcache_installed = False

class mcstats(object):
    
    def __init__(self, address, port):
        self.address = address
        self.port = port
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.address, self.port))
    
    def __del__(self):
        self.s.close()
        
    def connect(self, command):        
        num = self.s.send(command)        
        totalData = ''
        while True:
            data = self.s.recv(1024)
            if len(data) <= 0:
                break
            
            totalData = totalData + data
            if totalData.find('END') >= 0:
                break
        return totalData
        
    def calcSlabsCount(self, data):
        f = StringIO.StringIO(data)
        tmp = None
        for a in f:
            
            if a.find('END') >= 0:
                break
            else:
                tmp = a
        f.close()
        if tmp != None:
            return int(tmp.split(":")[1])
        else:
            return 0
        
    def showKVpairs(self, slabCounts, command="stats cachedump "):
        for a in range(0, slabCounts):
            tmpc = command + str(a + 1) + ' 0 \r\n'
            data = self.connect(tmpc)
            f = StringIO.StringIO(data)
            for b in f:
                if b.find('ITEM') >= 0:
                    arr = b.split(' ')
                    yield arr[1] , arr[2][1:len(arr[2])]        
            f.close()


def get_memcached_stats(server):
    if not memcache_installed:
        return {}
    host = memcache._Host(server)
    host.connect()
    host.send_cmd("stats")    
    stats = {}    
    while True:
        try:
            stat, key, value = host.readline().split(None, 2)
        except ValueError:
            break
        try:
            # Convert to native type, if possible
            value = int(value)
            if key == "uptime":
                value = datetime.timedelta(seconds=value)
            elif key == "time":
                value = datetime.datetime.fromtimestamp(value)
        except ValueError:
            pass
        stats[key] = value

    host.close_socket()    
    try:
        stats['hit_rate'] = 100 * stats['get_hits'] / stats['cmd_get']
    except ZeroDivisionError:
        stats['hit_rate'] = stats['get_hits']
    
    return stats

###############################################################################
##the function below is not for this app but useful for the use of memcache
###############################################################################
def cache_set(key, value):
    cache.set(key, value)
    return value


def cached_key_method(func):
    """
    this function is used to define the key using the argument inputed
    this define two,you can define all or some  of the argument as you wish
    sample like this :
        
    @cached_key_method
    def get_result(arg1,arg2):
        //your logic here    
        return result     
    """
    def cached_func(*args, **kwargs): 
        key = 'game::list::%s::%s'%(args[0],args[1])
        return cache.get(key) or cache_set(key, func(*args, **kwargs))

    return cached_func

def cached(key_input):
    """
    this fuction  recieve an argument, which is to be the key in memcache
    sample like this:
        
    @cached("key")
    def get_result():
        //your logic here
        return result
       
    """
    def _cached(func):
        def wrapper(*args, **kwargs):
            key = key_input
            return cache.get(key) or cache_set(key, func(*args, **kwargs))            
        return wrapper
    return _cached
