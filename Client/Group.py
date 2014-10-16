from Peer import Peer
import Shared

class Group:
    def __init__(self, id, name, members):
        self.id = id
        
        self.members = [] #list of Peer objects
        for member in members:
            peer = Shared.get_peer_by_username(member)
            if peer:
                self.members.append(peer)
            else:
                peer = Peer(member)
                Shared.peers_list.append(peer)
                self.members.append(peer)
        
        self.name = name
        
        Shared.main_window.calls.put((Shared.main_window.append_active_chat, name))
    
    def message(self, content):
        print 'message added to group ' + str(self.id) + ': ' + str(content)
        msg = Message.Message(Shared.my_data.username, content, group_id=self.id)
        
        for peer in self.members:
            peer.message(msg)
            
        self.data.append_message_to_chat(msg)
        Shared.main_window.calls.put((Shared.main_window.append_chat_message, self.id, msg))

    def message(self, msg):
        for peer in self.members:
            peer.message(msg)