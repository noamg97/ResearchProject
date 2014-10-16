my_data = None
server = None
peers_list = []
main_window = None

def get_peer_by_username(username):
    '''returns a Peer object if user is on either peers_list, else returns None'''
    for peer in peers_list:
        if peer.username == username:
            return peer