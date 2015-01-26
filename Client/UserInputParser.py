import OpCodes
import Friend
import Shared

def connect_to_peer(username):
    Shared.server.message(OpCodes.connect_to_peer, username)
 
def send_message(username, msg):
    friend = Shared.get_peer_by_username(username)
    if friend:
        friend.message(msg)
    else:
        print 'User ' + friend + ' not on friends list'

def state_changed(state):
    Shared.server.message(OpCodes.my_state_changed, str(state))
        
def send_friend_request(friend):
    friend = str(friend).strip()
    if friend in Shared.friends_list:
        print 'user ' + friend + " is already in your friends list"
        return
    Shared.server.message(OpCodes.send_friend_request, friend)

def accept_friend_request(friend):
    Shared.server.message(OpCodes.accept_friend_request, friend)
    Shared.friends_list.append(Friend.Friend(friend))
    Shared.main_window.calls.put((Shared.main_window.append_friend, friend))

def decline_friend_request(friend):
    Shared.server.message(OpCodes.decline_friend_request, friend)