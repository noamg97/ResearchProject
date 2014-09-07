import Friend
import Shared
import OpCodes
import MessageParser
import UserData
import Paths
import socket
import Queue
import sys


class Server:
    server_address = (socket.gethostbyname(socket.gethostname()), 4590) #TODO: get real address

    def __init__(self):
        if len(sys.argv) == 2: Server.server_address = (sys.argv[1], Server.server_address[1])
        if len(sys.argv) == 3: Server.server_address = (sys.argv[1], int(sys.argv[2]))
    
        self.outgoing_messages = Queue.Queue()
        self.create_new_socket(1)
        self.sleeping_sockets = []
    
    def message(self, action, value):
        print 'message added to outgoing queue: ' +str(action) + str(value) + ';'
        self.outgoing_messages.put(str(action) + str(value) + ';')
        
    def update(self):
        #check for messages from server
        try:
            data = self.sock.recv(512) #TODO: change to server's max possible message length
            if data:
                while not data.endswith(';'):
                    data += self.sock.recv(1)
                messages = [m for m in data.split(';') if m != '']
                for m in messages:
                    MessageParser.parse(m)
                    #print 'Message from server: ' + m #TODO: delete this when all parsing functions are implemented
            else:
                Shared.main_window.calls.put((Shared.main_window.destroy,))
                print 'Server Disconnected'
        except socket.error:
            #since the socket is non-blocking, it will raise an error each time it doesn't receive any data
            pass
        
        #check outgoing messages queue
        while not self.outgoing_messages.empty():
            msg = self.outgoing_messages.get()
            self.sock.send(msg)
            print 'Sent message to server: ' + msg
            
    def create_new_socket(self, blocking=0):
        print 'Creating new server socket'
        self.sock = socket.socket()
        
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #if hasattr(socket, 'SO_REUSEPORT'): self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        
        self.sock.connect(Server.server_address)
        self.sock.setblocking(blocking) #so listen won't need it's own thread.
    
    def init_sleeping_sockets(self):
        for i in xrange(4): self.append_sleeping_socket()
    
    def append_sleeping_socket(self):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if hasattr(socket, 'SO_REUSEPORT'): s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        
        s.connect(Server.server_address)
        s.send(OpCodes.sleeping_socket_connection + Shared.my_data.username + ',' + Shared.my_data.password + ';')
        
        response = ''
        data_byte = s.recv(1)
        while data_byte != ';':
            response += data_byte
            data_byte = s.recv(1)
        
        if response == OpCodes.sleeping_socket_accepted:
            self.sleeping_sockets.append(s)
            print 'sleeping socket accepted'
        if response == OpCodes.sleeping_socket_declined:
            print 'sleeping socket declined'
            # if reaches here it probably means that username/password are wrong for some reason
            #TODO: maybe retry?
            s.close()
            del s
    
    def send_login_request(self, username, password, state):
        #TODO: add encryption and stuff
        msg = OpCodes.login + username + ',' + password + ';'
        print 'Sending login message: ' + msg
        self.sock.send(msg)
        
        response = self.recv_one_blocking()
        if response == OpCodes.login_accepted:
            print 'login accepted'
            
            Paths.init(username)
            
            frnds_list_msg = self.recv_one_blocking()
            #TODO: also check that there aren't any data files of non friends
            if frnds_list_msg[:OpCodes.num_char] == OpCodes.friends_list:
                f_list = frnds_list_msg[OpCodes.num_char:].split(',')
                for f in f_list:
                    frnd = Friend.Friend(f)
                    Shared.friends_list.append(frnd)
            
            self.sock.setblocking(0)
            self.message(OpCodes.my_state_changed, state)
            return True
        if response == OpCodes.login_declined:
            print 'login declined'
            return False
        
    def send_create_user_request(self, username, password):
        msg = OpCodes.user_creation + username + ',' + password + ';'
        print 'Sending create user message: ' + msg
        self.sock.send(msg)
        
        response = self.recv_one_blocking()
        
        if response == OpCodes.user_created:
            print 'user created'
            Paths.init(username)
            self.sock.setblocking(0)
            self.message(OpCodes.my_state_changed, 1)
            return True
        if response == OpCodes.user_creation_declined:
            print 'user creation declined'
            return False

    def recv_one_blocking(self):
        response = ''
        data_byte = self.sock.recv(1)
        while data_byte != ';':
            response += data_byte
            data_byte = self.sock.recv(1)
        print 'recv_one_blocking got: ', response
        return response
    
    def disconnect(self):
        print 'Disconnecting from server'
        self.sock.close()