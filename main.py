from Friend import Friend
from Server import *
from Paths import *
import os


friends_list = []


def load_friends():
    #go through the data folders and for each file load a friend
    folder_safety(friends_data_path)
    content = os.listdir(friends_data_path)
    for i in xrange(len(content)):
        cd = friends_data_path + slash + content[i]
        if not os.path.isdir(cd) and content[i].endswith(data_file_extension):
            friends_list.append(Friend(content[i].split('.')[0]))


            
            
            
            
if __name__ == '__main__':
    #init
    server = Server()
    server.message(OpCodes.state_changed, 'online')
    load_friends()
    
    
    #init GUI
    
    
    #unload resources
    server.disconnect()
    for frnd in friends_list:
        frnd.close_chat_data_file()