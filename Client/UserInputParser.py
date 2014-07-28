from Server import OpCodes
import Friend
import Shared

class UserInputParser:
    def parse(self, input):
        if input.strip() == 'exit':
            return True
        
        a = input.split(':')
        a[0] = a[0].lower().strip()
        a[1] = a[1].strip()
        
        
        #connect to friend: friend_username
        if a[0].startswith('connect to friend'):
            Shared.server.message(OpCodes.connect_to_friend, a[1])
        
        #send: friend_username: message to send
        elif a[0].startswith('send'):
            friend = Shared.get_friend_by_username(a[1])
            if friend:
                friend.message(input[input.find(':',input.find(':')+1) + 1:])
            else:
                print 'User ' + a[1] + ' not on friends list'
        
        #send friend request: friend_username
        elif a[0].startswith('friend request'):
            Shared.server.message(OpCodes.send_friend_request, a[1])
        
        #accept friend request: friend_username
        elif a[0].startswith('accept friend request'):
            Shared.server.message(OpCodes.accept_friend_request, a[1])
            Shared.friends_list.append(Friend.Friend(a[1], True))
        
        #decline friend request: friend_username
        elif a[0].startswith('decline friend request'):
            Shared.server.message(OpCodes.decline_friend_request, a[1])
            
        return False