import socket
from Memcache import Memcache
#import constants.HOST as HOST
#import constants.PORT as PORT
from main import *
from Memcache import *

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 5000        # Port to listen on
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)

        memcache = Memcache()

        while(True):
            data = conn.recv(1024)
            print(data)
            if not data:
                break
            response = memcached_process(memcache, data)
            #conn.sendall(data)



""" from flask import Flask

app = Flask(__name__)

@app.route("/get")
def get(self, key):
    return "Hello"

@app.route("/set")
def set(self, key, value):
    return("Helloset") """