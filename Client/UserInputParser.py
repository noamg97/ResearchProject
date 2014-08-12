from Server import OpCodes
import Friend
import Shared

#connect to friend: friend_username
def connect_to_friend(username):
    Shared.server.message(OpCodes.connect_to_friend, a[1])
 
#send: friend_username: message to send
def send_message(msg):
    friend = Shared.get_friend_by_username(a[1])
    if friend:
        friend.message(input[input.find(':',input.find(':')+1) + 1:])
    else:
        print 'User ' + a[1] + ' not on friends list'

#send friend request: friend_username
def send_friend_request(friend):
    Shared.server.message(OpCodes.send_friend_request, a[1])

#accept friend request: friend_username
def accept_friend_request(friend):
    Shared.server.message(OpCodes.accept_friend_request, a[1])
    Shared.friends_list.append(Friend.Friend(a[1], True))

#decline friend request: friend_username
def decline_friend_request(friend):
    Shared.server.message(OpCodes.decline_friend_request, a[1])