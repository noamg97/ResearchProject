import Message
import UserInputParser
import socket
import time
import Queue

class Peer:
    def __init__(self, username):
        self.username = username
        self.out_messages = Queue.Queue()
        self.sock = None
        self.is_connected = False
        self.tried_to_connect = False

    #hole punching
    def start_punching(self, his_ep):
        if self.sock and self.state:
            print 'start punching ' + self.username
            my_ep = self.sock.getsockname()
            self.sock.close()
            self.sock = socket.socket()
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, 'SO_REUSEPORT'): self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self.sock.setblocking(0)
            self.sock.bind(my_ep)
            self.sock.connect_ex(his_ep)
            start = time.time()
            
            while True:
                if not self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR):
                    print 'succeeded punching ' + self.username
                    self.is_connected = True
                    return
                if time.time() - start > 3: #TODO: maybe change number
                    print 'retrying to punch ' + self.username
                    self.sock.connect_ex(his_ep)
                    start = time.time()

                
                #TODO: maybe delete listening part ? [commented for now]
                #try:
                #    self.sock.listen(5)
                #    accepted = self.sock.accept()
                #    if accepted:
                #        conn, addr = accepted
                #        if addr[0] == ip and addr[1] == port:
                #            self.sock.close()
                #            self.sock = conn
                #except socket.error:
                #    pass
        else:
            raise Exception("no socket found to start punching")
        
    def update(self):
        if self.state and not self.tried_to_connect and not self.out_messages.empty() and not self.is_connected:
            self.tried_to_connect = True
            UserInputParser.connect_to_peer(self.username)
            
        #send & receive messages
        if self.sock and self.is_connected:
            try:
                data = self.sock.recv(512)
                if data:
                    while not data.endswith(';'):
                        data += u.sock.recv(1)
                    messages = [m for m in data.split(';') if m != '']
                    for m in messages:
                        msg = Message.Message.from_data(m)
                        self.handle_incoming_message(msg)
                        print msg.to_console()
                else:
                    self.sock.close()
                    self.sock = None
                    print 'friend ' + self.username + ' had disconnected'
                    self.is_connected = False
                    self.tried_to_connect = False
            except socket.error: pass


            try:
                while not self.out_messages.empty():
                    print 'sent message to', self.username
                    self.sock.send(self.out_messages.get().to_data() + ';')
            except socket.error:
                self.is_connected = False
    
    def handle_incoming_message(self, msg):
        pass
        
    def message(self, msg):
        self.out_messages.put(msg)
                
    def close(self):
        if self.sock and self.is_connected:
            self.sock.close()