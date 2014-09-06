import socket
import time
import sys


def init():
    global sock
    
    server_address = (socket.gethostbyname(socket.gethostname()), 4590)
    if len(sys.argv) == 2: Server.server_address = (sys.argv[1], Server.server_address[1])
    if len(sys.argv) == 3: Server.server_address = (sys.argv[1], int(sys.argv[2]))
    
    sock = socket.socket()

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, 'SO_REUSEPORT'): sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    
    sock.connect(server_address)
    
def get_peer():
    global sock
    
    data = sock.recv(512)
    ip = data[2:data.rfind('\'')]
    port = int(data[data.index(' ')+1 : data.index(')')])
    
    return (ip, port)
    
def punch(addr):
    global sock
    print 'punching', addr
    my_addr = sock.getsockname()
    sock.close()
    
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(my_addr)
    while sock.connect_ex(addr): pass
    print "punching succeeded"
    
    

if __name__ == "__main__":
    sock = None
    init()
    addr = get_peer()
    punch(addr)
    
    sock.send(raw_input())
    print "received:", sock.recv(512)