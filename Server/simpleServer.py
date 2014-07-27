import socket
import time
import thread
import urllib2 as ulib
import re

class User:
    def __init__(self, sock, id):
        self.sock = sock
        #TODO: load all from database & add all other userdata variables
        self.id = id
        self.state = 0
        self.friends_list = [] 


should_exit = False
users = []

def update(connections, users):
    global should_exit
    
    while not should_exit:
        for u in users:
            try:
                data = u.sock.recv(512)
                if data:
                    while not data.endswith(';'):
                        data += u.sock.recv(1)
                    messages = [m for m in data.split(';') if m != '']
                    for msg in messages:
                        #print 'received message from user ' + u.id + ': ' + msg
                        if msg[:2] == '02':
                            for usr in users:
                                if usr.id == msg[2:]:
                                    print 'user ' + u.id + ' starts connecting to ' + usr.id
                                    usr_ip, usr_port = usr.sock.getpeername()
                                    u_ip, u_port = u.sock.getpeername()
                                    u.sock.send('99' + str(usr.id) + ',' + str(usr_ip) + ',' + str(usr_port))
                                    usr.sock.send('99' + str(u.id) + ',' + str(u_ip) + ',' + str(u_port))
                        if msg[:2] == '00':
                            print 'user ' + u.id + ' is now ' + msg[2:].strip()
                            u.status = int(msg[2:])
                                
                else:
                    print u.id + ' disconnected'
                    u.sock.close()
                    users.remove(u)
            except socket.error: pass

        for c in connections:
            try:
                data = c.recv(1)
                if data:
                    msg = ''
                    while data != ';':
                        msg += data
                        data = c.recv(1)
                        
                    if msg[:2] == '05':
                        user_id = msg[2:].strip()
                        print 'user ' + user_id + ' logged in from ' + str(c.getpeername())
                        users.append(User(c, user_id))
                        connections.remove(c)
                else:
                    c.close()
                    connections.remove(c)
            except socket.error: pass
        time.sleep(1.0/60.0)


    for c in connections:
        c.close()
    for u in users:
        u.close()


data = ulib.urlopen('http://www.ipchicken.com/').read()
external_ip = re.search("\\d{1,3}\\.\\d{1,3}\\.\d{1,3}\\.\\d{1,3}", data).group()
external_port =  re.search("Port: \d*", data).group()[len('Port: '):]
print 'extarnal endpoint: ' + external_ip + ':' + external_port

s = socket.socket()
s.bind((socket.gethostbyname(socket.gethostname()), 4590))
my_ip, my_port = s.getsockname()
print 'internal endpoint: ' + my_ip + ':' + str(my_port)
print '\n------------\n'
s.listen(5)
connections = []

thread.start_new_thread(update, (connections,users))

try:
    while True:
        c, a = s.accept()
        c.setblocking(0)
        connections.append(c)
        print 'connected: ', a
except KeyboardInterrupt:
    should_exit = True
    print 'exiting'
