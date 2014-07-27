my_id = ''
server = None
friends_list = []

def get_friend_by_id(id):
    for fr in friends_list:
        if fr.data.id == id:
            return fr

def get_username_from_id(id):
    for fr in friends_list:
        if fr.data.id == id:
            return fr.data.profile_data['username']