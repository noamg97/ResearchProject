from Server import OpCodes
import Shared

class UserInputParser:
    def parse(self, input):
        a = input.split(':')
        a[0] = a[0].lower().strip()
        a[1] = a[1].strip()
        
        #connect to friend: friend_id
        if a[0].startswith('connect to friend'):
            Shared.server.message(OpCodes.connect_to_friend, a[1])
        
        #send: friend's id: message to send
        if a[0].startswith('send'):
            friend = Shared.get_friend_by_id(a[1])
            if friend:
                friend.message(input[input.find(':',input.find(':')+1) + 1:])
            else:
                print 'User ' + a[1] + ' not on friends list'