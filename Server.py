import threading
import socket
import Queue

class OpCodes:
    num_char = 2 #how many characters in an opcode

    state_changed = '00'
    connect_to_friend = '01'        #TODO: add more
    fname_changed = '02'
    lname_changed = '03'
    
    @staticmethod
    def get_action_by_opcode(opcode):
        for action, op in vars(OpCodes).iteritems():
            if str(op) == str(opcode):
                return str(action)
        return ''

    
    
class Server:
    server_address = ('127.0.0.1', 4590) #TODO: get real address

    def __init__(self):
        self.outgoing_messages = Queue.Queue()
        self.incoming_messages = Queue.Queue()
        self.sock = socket.socket()
        self.sock.connect(server_address)
        self.sock.setblocking(0) #so listen won't need it's own thread.

    def message(self, action, value):
        self.outgoing_messages.put(action + value)
        
    def update(self):
        #check for messages from server
        try:
            data = self.sock.recv(512) #TODO: change to smaller number ?
            if not data: raise Exception('Server Disconnected')
            incoming_messages.put(data)
        except socket.error:
            #since the socket is non-blocking, it will raise an error each time it doesn't receive any data
            pass
        
        #check outgoing messages queue
        while not outgoing_messages.empty():
            self.sock.send(self.outgoing_messages.get())
            
            
    def disconnect(self):
        self.sock.close()