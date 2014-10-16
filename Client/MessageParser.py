import OpCodes
import Friend
import threading
import Shared

def parse(message):
    opcode = message[:OpCodes.num_char]
    value = message[OpCodes.num_char:]
    
    if opcode == OpCodes.friend_connecting:
       parse_friend_connecting(value)
    elif opcode == OpCodes.friend_state_changed:
        parse_friend_state_changed(value)
    elif opcode == OpCodes.friend_request:
        parse_friend_request(value)
    elif opcode == OpCodes.friend_request_accepted:
        parse_friend_request_accepted(value)
    elif opcode == OpCodes.friend_request_declined:
        parse_friend_request_declined(value)
        
    #TODO: add more


#friend_username,ip,port
def parse_friend_connecting(value):
    a = value.split(',')
    friend_username = a[0]
    ip = a[1]
    port = a[2]
    print 'friend connecting: ' + friend_username + ' at ' + ip + ':' +  port
    
    friend = Shared.get_peer_by_username(friend_username)
    if friend:
        friend.sock = Shared.server.sleeping_sockets[0]
        Shared.server.sleeping_sockets.pop(0)
        friend.sock.setblocking(0)
        threading.Thread(target=friend.start_punching, args=[(ip, int(port))]).start()
        Shared.server.append_sleeping_socket() # TODO: maybe move into that thread ^
    else:
        print 'Connecting friend is not on friends list'
    
    
#friend_username,state_code
def parse_friend_state_changed(value):
    friend_username, state = value.split(',')
    friend = Shared.get_peer_by_username(friend_username)
    if friend:
        friend.change_state(state)
    
#friend_username
def parse_friend_request(value):
    print 'User ' + value + ' has sent you a friend request'
    Shared.main_window.calls.put((Shared.main_window.append_frequest, value))
    print Shared.main_window.calls
    
#friend_username
def parse_friend_request_accepted(value):
    print 'User ' + value + ' has accepted your friend request'
    Shared.friends_list.append(Friend.Friend(value, True))
    Shared.main_window.calls.put((Shared.main_window.append_friend, value))
    
#friend_username
def parse_friend_request_declined(value):
    print 'User ' + value + ' declined your friend request'
    
#group_id,group_name,member1_id,...,memberN_id
def parse_added_to_group(value):
    