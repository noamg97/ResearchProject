import Database
import OpCodes
import MessageParser
import time
import urllib2 as ulib
import socket
import threading
import select



def server_thread():
    global users_sockets, should_exit
    while not should_exit:
        for username in users_sockets.keys():
            #check the active socket for data
            try:
                data = users_sockets[username][0].recv(512)
                if data:
                    while not data.endswith(';'):
                        data += users_sockets[username][0].recv(1)
                    messages = [m for m in data.split(';') if m != '']
                    for msg in messages:
                        print 'got message from user '+ username+ ' : '+ msg
                        MessageParser.parse(msg, username)
                else:
                    print username + "'s main socket disconnected"
                    MessageParser.parse_user_state_changed(0, username)
                    for s in users_sockets[username]: s.close()
                    users_sockets.pop(username, None)
                    continue
            except socket.error: pass
            
            #check all the sleeping sockets for disconnection
            ready_to_read, wr, er = select.select(users_sockets[username], [], [], 0)
            for sock in ready_to_read:
                try:
                    if not sock.recv(2):
                        print 'a sleeping socket from ' + username + ' had disconnected'
                        sock.close()
                        users_sockets[username].remove(sock)
                except socket.error: pass
                
                
        time.sleep(1.0/60.0)
    print 'server thread ended'    
        
        
        
        
#username,password
def login(data, sock):
    global db, users_sockets
    
    username, password = data.split(',')
    print 'got login request from user ' + username + ' with password ' + password
    
    if db.validate_password(username, password):
        print 'user ' + username + ' had logged in successfully'
        sock.setblocking(0)
        users_sockets[username] = [sock]
        sock.send(OpCodes.login_accepted + ';')
        MessageParser.parse_user_state_changed(1, username)
        
        #send all messages from queued_messages.
        queued_msgs = db.get_list_from_field(username, 'queued_messages')
        if queued_msgs:
            sock.send(';'.join(queued_msgs) + ';')
            db.set_field(username, 'queued_messages', '')
    else:
        print 'login from user ' + username + ' is invalid'
        sock.send(OpCodes.login_declined + ';')
    
    
#username,password
def create_user(data, sock):
    global db, users_sockets
    
    username, password = data.split(',')
    if not db.does_user_exist(username):
        db.insert_new_user(username, password)
        sock.setblocking(0)
        users_sockets[username] = [sock]
        sock.send(OpCodes.user_created + ';')
    else:
        sock.send(OpCodes.user_creation_declined + ';')

        
def append_sleeping_socket(data, sock):
    global db, users_sockets
    
    username, password = data.split(',')
    
    if db.validate_password(username, password):
        print 'sleeping socket from ' + username + ' added'
        users_sockets[username].append(sock)
        sock.send(OpCodes.sleeping_socket_accepted + ';')
    else:
        print 'sleeping socket request from user ' + username + ' failed'
        sock.send(OpCodes.sleeping_socket_declined + ';')
    

    
def new_connections_listener():
    global connections, main_socket, should_exit
    try:
        while True:
            ready_to_read, wr, er = select.select(connections, [], [], 0)
            for sock in ready_to_read:
                if sock is main_socket:
                    c, a = sock.accept()
                    connections.append(c)
                    print 'connection from: ', a
                    
                else:
                    try:
                        msg = sock.recv(1)
                        if not msg:
                            sock.close()
                            connection.remove(sock)
                        
                        while not msg.endswith(';'):
                            msg += sock.recv(1)
                    except socket.error:
                        connections.remove(sock)
                        continue
                        
                    msg = msg[:len(msg)-1]
                    
                    if msg[:OpCodes.num_char] == OpCodes.login:
                        login(msg[OpCodes.num_char:], sock)
                    elif msg[:OpCodes.num_char] == OpCodes.user_creation:
                        create_user(msg[OpCodes.num_char:], sock)
                    elif msg[:OpCodes.num_char] == OpCodes.sleeping_socket_connection:
                        append_sleeping_socket(msg[OpCodes.num_char:], sock)
                    else: #invalid opcode, so don't remove the socket from connection
                        continue
                        
                    connections.remove(sock)
                    
    except KeyboardInterrupt:
        should_exit = True
        print 'exiting...'

        
        
        
if __name__ == "__main__":
    external_ip = ulib.urlopen('http://bot.whatismyipaddress.com').read()
    print 'extarnal ip: ' + external_ip

    #TODO: maybe use separate socket for user creation
    
    main_socket = socket.socket()
    main_socket.bind((socket.gethostbyname(socket.gethostname()), 4590))
    my_ip, my_port = main_socket.getsockname()
    print 'internal endpoint: ' + my_ip + ':' + str(my_port)
    print '\n\n------------\n'
    main_socket.listen(5)
    
    connections = [main_socket]
    users_sockets = {} # { 'username': [active socket, sleeping socket1, ..., sleeping socketN] }
    should_exit = False
    db = Database.Database(users_sockets)
    MessageParser.init(db, users_sockets)
    
    t = threading.Thread(target=server_thread)
    t.start()
    
    new_connections_listener()
    
    print 'unloading resources...'
    t.join()
    for con in connections:
        con.close()
    for sock in users_sockets.values():
        sock.close()
    main_socket.close()
    db.close()
    
    print 'done.'