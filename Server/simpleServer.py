import socket
import time
import thread
import urllib2 as ulib
import re
import sqlite3 as sql

#TODO: load from database & add all other userdata variables
class User:
    def __init__(self, sock, username, password):
        self.sock = sock
        
        self.username = username
        self.password = password
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
    global db
    
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
                            u.state = int(msg[2:])
                        elif msg[:2] == '01':
                            print 'user ' + u.username + ' asked for ' + msg[2:] + "'s state"
                            usr = get_user_by_username(msg[2:])
                            if usr:
                                u.sock.send('97' + str(usr.state) + ';')
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
                        username, password = [ x.strip() for x in msg[2:].split(',') ]
                        print 'user ' + username + ' logged in with password ' + password + ' from ' + str(c.getpeername())
                        usr = get_user_by_username(username)
                        if usr:
                            if usr.password == password:
                                usr.sock = c
                                usr.sock.setblocking(0)
                                usr.state = 1
                                connections.remove(c)
                                
                            else:
                                c.send('92;')
                    elif msg[:2] == '09':
                        username, password = [ x.strip() for x in msg[2:].split(',') ]
                        print 'creating user "' + username + '" with password "' + password '"'
                        usr = get_user_by_username(username)
                        if not usr:
                            db.execute("INSERT INTO users(username, password) VALUES (?);", (username, password))
                else:
                    c.close()
                    connections.remove(c)
            except socket.error: pass
        time.sleep(1.0/60.0)


    for c in connections:
        c.close()
    for u in users:
        u.close()


        
        
external_ip = ulib.urlopen('http://bot.whatismyipaddress.com').read()
print 'extarnal ip: ' + external_ip

s = socket.socket()
s.bind((socket.gethostbyname(socket.gethostname()), 4590))
my_ip, my_port = s.getsockname()
print 'internal endpoint: ' + my_ip + ':' + str(my_port)
print '\n------------\n'
s.listen(5)
connections = []



db = sql.connect('database.db')
c = db.cursor()
c.execute("create table if not exists users (username text, password text)")
c.execute("SELECT * FROM users")
rows = c.fetchall()
if rows:
    for row in rows:
        users.append(User(None, row[0], row[1]))


thread.start_new_thread(update, (connections,users))

try:
    while True:
        c, a = s.accept()
        connections.append(c)
        print 'connected: ', a
except KeyboardInterrupt:
    should_exit = True

print 'exiting'
db.commit()
db.close()
