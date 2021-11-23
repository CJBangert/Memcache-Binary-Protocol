import socket
from Memcache import Memcache
from main import *
from Memcache import *

from _thread import *


#instatiate cache
memcache = Memcache()


threadLock = threading.Lock()

def Main():

    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 5000        # Port to listen on

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((HOST, PORT))
    
    #5 is suggested num of non-accepted outstanding connections
    s.listen(5)
    
    while(True):
        conn, addr = s.accept()

        threadLock.acquire()
        print('Connected by', addr, flush=True)
        start_new_thread(threaded,(conn,))

        

    s.close() 

 

def threaded(conn):
    while(True):
        data = conn.recv(1024)

        print("Incoming: ", data, flush=True)

        if not data:

            print("End of stream...", flush=True)

            #release lock on exit
            threadLock.release()

            break
        try:    
            response = memcached_process(memcache, data)

        except UnsupportedOperation:
            response = str_to_bytes("Unsupported op")

        
        conn.send(response)
        

    conn.close()
        

    


if __name__ == '__main__':
    Main()
