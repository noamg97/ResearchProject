import socket
import Queue

class OpCodes:
    num_char = 2 #how many characters in an opcode

    #incoming
    friend_connecting = '99'
    friend_endpoint_changed = '98'
    friend_status_changed = '97'

    
    #outgoing
    my_state_changed = '00'
    ask_for_status = '01'
    connect_to_friend = '02'        #TODO: add more
    fname_changed = '03'
    lname_changed = '04'
    login = '05'
    
    @staticmethod
    def get_action_by_opcode(opcode):
        for action, op in vars(OpCodes).iteritems():
            if str(op) == str(opcode):
                return str(action)
        return ''

    
    
class Server:
    server_address = (socket.gethostbyname(socket.gethostname()), 4590) #TODO: get real address

    def __init__(self, my_id):
        self.my_id = my_id
        self.outgoing_messages = Queue.Queue()
        self.incoming_messages = Queue.Queue()
        self.create_new_socket()
        self.login()
    
    def message(self, action, value):
        self.outgoing_messages.put(str(action) + str(value) + ';')
        
    def update(self):
        #check for messages from server
        try:
            data = self.sock.recv(512) #TODO: change to server's max possible message length
            if not data: raise Exception('Server Disconnected')
            self.incoming_messages.put(data)
            print 'Message from server: ' + data #TODO: delete this when all parsing functions are implemented
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
        print 'Sending login message: ' + OpCodes.login + self.my_id
        self.sock.send(OpCodes.login + self.my_id + ';')
        #TODO: add encryption and stuff

    def disconnect(self):
        print 'Disconnecting from server'
        self.sock.close()