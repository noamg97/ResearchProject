my_data = None
server = None
friends_list = []
main_window = None

def get_peer_by_username(username):
    '''returns a Peer object if user is on friends_list, else returns None'''
    for peer in friends_list:
        if peer.username == username:
            return peer