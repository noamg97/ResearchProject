import Shared
import socket
import Queue
import sys

class OpCodes:
    num_char = 2 #how many characters in an opcode
    
    #____Not Logged In:____#
    
    #incoming
    login = '00'
    user_creation = '01'

    #outgoing
    login_accepted = '99'
    login_declined = '98'
    user_created = '97'
    user_creation_declined = '96'
    
    

    
    #____Logged In Users:____#

    #outgoing
    my_state_changed = '00'
    connect_to_friend = '01'
    profile_data_changed = '02'
    send_friend_request = '03'
    accept_friend_request = '04'
    decline_friend_request = '05'
    
    #incoming
    friend_connecting = '99'
    friend_state_changed = '98'
    friend_request = '97'
    friend_request_accepted = '96'
    friend_request_declined = '95'
    
    
    @staticmethod
    def get_action_by_opcode(opcode):
        for action, op in vars(OpCodes).iteritems():
            if str(op) == str(opcode):
                return str(action)
        return ''

    
    
class Server:
    server_address = (socket.gethostbyname(socket.gethostname()), 4590) #TODO: get real address

    def __init__(self):
        if len(sys.argv) == 2: Server.server_address = (sys.argv[1], Server.server_address[1])
        if len(sys.argv) == 3: Server.server_address = (sys.argv[1], int(sys.argv[2]))
    
        self.outgoing_messages = Queue.Queue()
        self.incoming_messages = Queue.Queue()
        self.create_new_socket()
        if Shared.my_data.is_new_user:
            self.create_user()
        self.login()
    
    def message(self, action, value):
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
                    self.incoming_messages.put(m)
                    print 'Message from server: ' + data #TODO: delete this when all parsing functions are implemented
            else: 
                raise Exception('Server Disconnected')
        except socket.error:
            #since the socket is non-blocking, it will raise an error each time it doesn't receive any data
            pass
        
        #check outgoing messages queue
        while not self.outgoing_messages.empty():
            msg = self.outgoing_messages.get()
            self.sock.send(msg)
            print 'Sent message to server: ' + msg
            
    def create_new_socket(self):
        print 'Creating new server socket'
        self.sock = socket.socket()
        
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if hasattr(socket, 'SO_REUSEPORT'): self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        
        self.sock.connect(Server.server_address)
        self.sock.setblocking(0) #so listen won't need it's own thread.
    
    def login(self):
        msg = OpCodes.login + Shared.my_data.username + ',' + Shared.my_data.password + ';'
        print 'Sending login message: ' + msg    
        self.message(OpCodes.my_state_changed, stateCodes.online)

        self.sock.send(msg)
        #TODO: add encryption and stuff
    
    def create_user(self):
        msg = OpCodes.create_user + Shared.my_data.username + ',' + Shared.my_data.password + ';'
        print 'Sending create user message: ' + msg
        self.sock.send(msg)

    
    def disconnect(self):
        print 'Disconnecting from server'
        self.sock.close()