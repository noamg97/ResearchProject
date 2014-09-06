import urllib2 as ulib
import socket
import thread


def init():
    global s
    
    print 'extarnal ip: ' + ulib.urlopen('http://bot.whatismyipaddress.com').read()

    s = socket.socket()
    s.bind((socket.gethostbyname(socket.gethostname()), 4590))
    my_ip, my_port = s.getsockname()
    print 'internal endpoint: ' + my_ip + ':' + str(my_port)
    print '\n------------\n'
    s.listen(5)


if __name__ == "__main__":
    s = None
    
    init()
    
    try:
        while True:
            sock1, addr1 = s.accept()
            print 'connected: ', addr1
            sock2, addr2 = s.accept()
            print 'connected: ', addr2
            
            sock1.send(str(addr2))
            sock2.send(str(addr1))
            
            print '\n'
            
    except KeyboardInterrupt:
        should_exit = True
