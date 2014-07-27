from Server import OpCodes
import threading
import Shared

class MessageParser:
    def parse(self, message):
        opcode = message[:OpCodes.num_char]
        value = message[OpCodes.num_char:]
        
        if opcode == OpCodes.friend_connecting:
            self.parse_friend_connecting(value)
        if opcode == OpCodes.friend_status_changed:
            self.parse_friend_status_changed(value)
        
        #TODO: add more
    
    
    #friend_id,ip,port
    def parse_friend_connecting(self, value):
        a = value.split(',')
        id = a[0]
        ip = a[1]
        port = a[2]
        print 'friend connecting: ' + id + ' at ' + ip + ':'+  port
        
        friend = Shared.get_friend_by_id(id)
        if friend:
            friend.sock = Shared.server.sock
            Shared.server.create_new_socket()
            Shared.server.login()
            threading.Thread(target=friend.start_punching, args=[(ip, int(port))]).start()
        else:
            print 'Connecting friend is not on friends list'
        
        
    #'friend_id,status_code'
    def parse_friend_status_changed(self, value):
        id, status = value.split(',')
        friend = Shared.get_friend_by_id(id)
        if friend:
            print 'friend ' + id + ' is now ' + status
            friend.change_status(status)