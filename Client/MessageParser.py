from Server import OpCodes
import Friend
import threading
import Shared

class MessageParser:
    def parse(self, message):
        opcode = message[:OpCodes.num_char]
        value = message[OpCodes.num_char:]
        
        if opcode == OpCodes.friend_connecting:
            self.parse_friend_connecting(value)
        elif opcode == OpCodes.friend_status_changed:
            self.parse_friend_status_changed(value)
        elif opcode == OpCodes.friend_request:
            self.parse_friend_request(value)
        elif opcode == OpCodes.friend_request_accepted:
            self.parse_friend_request_accepted(value)
        elif opcode == OpCodes.friend_request_declined:
            self.parse_friend_request_declined(value)
            
            
        #TODO: add more
    
    
    #friend_username,ip,port
    def parse_friend_connecting(self, value):
        a = value.split(',')
        friend_username = a[0]
        ip = a[1]
        port = a[2]
        print 'friend connecting: ' + friend_username + ' at ' + ip + ':'+  port
        
        friend = Shared.get_friend_by_username(friend_username)
        if friend:
            friend.sock = Shared.server.sock
            Shared.server.create_new_socket()
            Shared.server.login()
            threading.Thread(target=friend.start_punching, args=[(ip, int(port))]).start()
        else:
            print 'Connecting friend is not on friends list'
        
        
    #friend_username,status_code
    def parse_friend_status_changed(self, value):
        friend_username, status = value.split(',')
        friend = Shared.get_friend_by_username(friend_username)
        if friend:
            print 'Friend ' + friend_username + ' is now ' + status
            friend.change_status(status)
        
    #friend_username
    def parse_friend_request(self, value):
        print 'User ' + value + ' has sent you a friend request'
        
    #friend_username
    def parse_friend_request_accepted(self, value):
        print 'User ' + value + ' has accepted your friend request'
        Shared.friends_list.append(Friend.Friends(value, True))
        
    #friend_username
    def parse_friend_request_declined(self, value):
        print 'User ' + value + ' declined your friend request'

        
        
        
        