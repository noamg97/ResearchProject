import threading
import socket
import Queue

class OpCodes:
    self.state_changed = '00'
    self.connect_to_friend = '01'        #TODO: add more
    self.fname_changed = '02'
    self.lname_changed = '03'
        
    def get_action_by_opcode(opcode):
        for action, op in vars(OpCodes).iteritems():
            if op == opcode:
                return action
        return ''

class Server:
    server_address = ('127.0.0.1', 4590)

    def __init__(self):
        self.outgoing_messages = Queue.Queue()
        self.exit = False
        self.sock = socket.socket()
        self.sock.setblocking(0) #so listen won't need it's own thread.
        self.sock.connect(server_address)
        self.main_loop_thread = threading.Thread(target=self.main_loop)
        self.main_loop_thread.deamon = True #won't keep the process up if main thread ends. not really necessary
        self.main_loop_thread.start()

    def message(self, action, value):
        self.outgoing_messages.put(action + value)
        
    def main_loop(self):
        while not self.exit:
            #check for messages from server
            data = self.sock.recv(512) #TODO: change to smaller number ?
            if not data: raise error('Server Disconnected')
            parse_message(data)
            
            #check outgoing messages queue
            while not outgoing_messages.empty():
                self.sock.send(self.outgoing_messages.get())
                
    def parse_message(self, message)
        op = message[:2] #TODO: change opcode length accordingly 
        value = message[2:] #same
        action = ''
        
        action = OpCodes.get_action_by_opcode(op)
        if action == '':
            raise error('no opcode specified in message')
        
        #do whatever the message asks
        
    def disconnect(self):
        self.exit = True
        self.main_loop_thread.join()
        self.sock.close()