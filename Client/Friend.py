import UserData
import Message
import Shared
import UserInputParser
from Server import OpCodes
import socket
import time
import Queue

class StateCodes:
    offline = 0; online = 1; afk = 2; busy = 3
    
    @staticmethod
    def get_state_by_code(code):
        for _state, _code in vars(StateCodes).iteritems():
            if str(_code) == str(code):
                return str(_state)
        raise Exception("No state matches state code " + code)
        
    @staticmethod
    def get_code_by_state(state):
        for _state, _code in vars(StateCodes).iteritems():
            if str(_state) == str(state):
                return _code
        raise Exception("No state code matches state " + state)

        
class Friend:
    def __init__(self, username):
        self.state = StateCodes.offline
        self.data = UserData.UserData(username)
        self.out_messages = Queue.Queue()
        self.sock = None
        self.is_connected = False
        self.tried_to_connect = False

    
    #hole punching
    def start_punching(self, his_ep):
        if self.sock and self.state:
            print 'start punching ' + self.data.username
            my_ep = self.sock.getsockname() #TODO: check if this actually works on NAT, maybe router gives me a new ext_ep although the int_ep is the same
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
                    print 'succeeded punching ' + self.data.username
                    self.is_connected = True
                    return
                if time.time() - start > 3: #maybe change number
                    print 'retrying to punch ' + self.data.username
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
        if self.state and not self.tried_to_connect and not self.out_messages.empty() and not self.is_connected:
            self.tried_to_connect = True
            UserInputParser.connect_to_friend(self.data.username)
            
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
                        self.data.append_message_to_chat(msg)
                        Shared.main_window.calls.put((Shared.main_window.append_chat_message, self.data.username, msg))
                        print msg.to_console()
                else:
                    self.sock.close()
                    self.sock = None
                    print 'friend ' + self.data.username + ' had disconnected'
                    self.is_connected = False
                    self.tried_to_connect = False
            except socket.error: pass


            try:
                while not self.out_messages.empty():
                    self.sock.send(self.out_messages.get().to_data() + ';')
            except socket.error:
                self.is_connected = False
                

        
    def message(self, content):
        print 'message added to friend ' + str(self.data.username) + ': ' + str(content)
        msg = Message.Message(Shared.my_data.username, content)
        self.out_messages.put(msg)
        self.data.append_message_to_chat(msg)
        Shared.main_window.calls.put((Shared.main_window.append_chat_message, self.data.username, msg))
        
    def change_state(self, state):
        print self.data.username + ' is now ' + StateCodes.get_state_by_code(state)
        self.state = int(state)
        Shared.main_window.calls.put((Shared.main_window.friend_state_changed, self.data.username, StateCodes.get_state_by_code(state)))
        
        
    def get_chat(self):
        return self.data.chat_data
        
    def close(self):
        if self.sock and self.is_connected:
            self.sock.close()
        self.data.close_chat_data_file()