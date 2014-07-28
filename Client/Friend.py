import UserData
import Message
import Shared
from Server import OpCodes
import socket
import time
import Queue

class StatusCodes:
    offline = 0; online = 1; afk = 2; dont_disturb = 3
    
    @staticmethod
    def get_status_by_code(code):
        for _status, _code in vars(StatusCodes).iteritems():
            if str(_code) == str(code):
                return str(_status)
        return ''


class Friend:
    def __init__(self, username, is_new=False):
        if is_new:
            UserData.UserData.create_files(username)
        
        self.status = StatusCodes.offline
        self.data = UserData.UserData(username)
        self.out_messages = Queue.Queue()
        self.sock = None
        self.is_connected = False

        #ask the server for his current status
        Shared.server.message(OpCodes.request_status, username)

            
    
    #hole punching
    def start_punching(self, his_ep):
        if self.sock:
            print 'start punching ' + self.data.profile_data['username']
            my_ep = self.sock.getsockname() #TODO: check if this actually works on NAT, maybe router gives me a new ext_ep although the int_ep is the same
            self.sock.close()
            self.sock = socket.socket()
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.setblocking(0)
            self.sock.bind(my_ep)
            self.sock.connect_ex(his_ep)
            start = time.time()
            
            while True:
                if not self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR):
                    print 'succeeded punching ' + self.data.profile_data['username']
                    self.is_connected = True
                    return
                if time.time() - start > 3: #maybe change number
                    print 'retrying to punch ' + self.data.profile_data['username']
                    self.sock.connect_ex(his_ep)
                    start = time.time()

                
                #maybe delete listening part ? [probably..][commented for now]
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
        if self.sock and self.is_connected:
            #send & receive messages
            while not self.out_messages.empty():
                self.sock.send(self.out_messages.get().to_data() + ';')
                
            try:
                data = self.sock.recv(512)
                if data:
                    while not data.endswith(';'):
                        data += u.sock.recv(1)
                    messages = [m for m in data.split(';') if m != '']
                    for m in messages:
                        msg = Message.Message.from_data(m.strip())
                        self.data.append_message_to_chat(msg)
                        print msg.to_readable()
                else:
                    self.sock.close()
                    self.is_connected = False
            except socket.error: pass

        
    def message(self, content):
        msg = Message.Message(Shared.my_data.username, content)
        self.out_messages.put(msg)
        self.data.append_message_to_chat(msg)
        
    def change_status(self, status):
        print self.data.profile_data['username'] + ' is now ' + StatusCodes.get_status_by_code(status)
        self.status = status
        #update GUI?
        
    def get_chat(self):
        return self.data.chat_data
        
    def close(self):
        if self.sock and self.is_connected:
            self.sock.close()
        self.data.close_chat_data_file()