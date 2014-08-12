my_data = None
server = None
friends_list = []

def get_friend_by_username(username):
    for fr in friends_list:
        if fr.data.username == username:
            return fr