from Peer import Peer
import UserData
import Shared

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

        
class Friend(Peer):
    def __init__(self, username):
        Peer.__init__(self, username)
        self.state = StateCodes.offline
        self.data = UserData.UserData(username)

    def message(self, content):
        print 'message added to friend ' + str(self.username) + ': ' + str(content)
        msg = Message.Message(Shared.my_data.username, content)
        Peer.message(self, msg)
        self.data.append_message_to_chat(msg)
        Shared.main_window.calls.put((Shared.main_window.append_chat_message, self.username, msg))
        
    def handle_incoming_message(self, msg):
        self.data.append_message_to_chat(msg)
        Shared.main_window.calls.put((Shared.main_window.append_chat_message, self.username, msg))
        
    def change_state(self, state):
        print self.username + ' is now ' + StateCodes.get_state_by_code(state)
        self.state = int(state)
        Shared.main_window.calls.put((Shared.main_window.friend_state_changed, self.username, StateCodes.get_state_by_code(state)))
        
    def get_chat(self):
        return self.data.chat_data
        
    def close(self):
        Peer.close(self)
        self.data.close_chat_data_file()