import socket
import time
import thread
import urllib2 as ulib
import re

#TODO: load from database & add all other userdata variables
class User:
    def __init__(self, sock, username):
        self.sock = sock
        
        self.username = username
        self.state = 0
        self.friends_list = [] #TODO: load from database


should_exit = False
users = []

def get_user_by_username(username):
    for u in users:
        if u.username == username:
            return u


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
                        if msg[:2] == '02':
                            usr = get_user_by_username(msg[2:])
                            if usr:
                                print 'user ' + u.username + ' starts connecting to ' + usr.username
                                usr_ip, usr_port = usr.sock.getpeername()
                                u_ip, u_port = u.sock.getpeername()
                                u.sock.send('99' + str(usr.username) + ',' + str(usr_ip) + ',' + str(usr_port) + ';')
                                usr.sock.send('99' + str(u.username) + ',' + str(u_ip) + ',' + str(u_port) + ';')
                        elif msg[:2] == '00':
                            print 'user ' + u.username + ' is now ' + msg[2:].strip()
                            u.status = int(msg[2:])
                        elif msg[:2] == '01':
                            print 'user ' + u.username + ' asked for ' + msg[2:] + "'s status"
                            usr = get_user_by_username(msg[2:])
                            if usr:
                                u.sock.send('96' + str(usr.state) + ';')
                        elif msg[:2] == '06':
                            print 'user ' + u.username + ' sent a friend request to user ' + msg[2:]
                            usr = get_user_by_username(msg[2:])
                            if usr:
                                usr.sock.send('96' + u.username + ';')
                            else: 
                                print 'user ' + msg[2:] + ' does not exist'
                                u.sock.send('94' + msg[2:] + ';')
                        elif msg[:2] == '07':
                            print 'user ' + u.username + ' accepted a friend request from user ' + msg[2:]
                            usr = get_user_by_username(msg[2:])
                            if usr:
                                usr.friends_list.append(u.username)
                                u.friends_list.append(usr.username)
                                usr.sock.send('95' + u.username + ';')
                        elif msg[:2] == '08':
                            print 'user ' + u.username + ' declined a friend request from user ' + msg[2:]
                            usr = get_user_by_username(msg[2:])
                            if usr:
                                usr.sock.send('94' + u.username + ';')
                else:
                    print u.username + ' disconnected'
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
                        username = msg[2:].strip()
                        print 'user ' + username + ' logged in from ' + str(c.getpeername())
                        users.append(User(c, username))
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
#external_port =  re.search("Port: \d*", data).group()[len('Port: '):]
print 'extarnal ip: ' + external_ip #+ ':' + external_port

s = socket.socket()
s.bind((socket.gethostbyname(socket.gethostname()), 4590))
#s.bind((external_ip, 4590))
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
