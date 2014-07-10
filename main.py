import Friend
import Server
import Paths
import os
import threading



def load_friends(friends_list):
    #go through the data folders and for each file load a friend
    folder_safety(friends_data_path)
    content = os.listdir(friends_data_path)
    for i in xrange(len(content)):
        cd = friends_data_path + slash + content[i]
        if not os.path.isdir(cd) and content[i].endswith(data_file_extension):
            friends_list.append(Friend.Friend(content[i].split('.')[0]))

            
def message_parser(message):
    opcode = message[:OpCodes.num_char]
    value = message[OpCodes.num_char:]
    
    if opcode == '00'
    
            
def main_loop(server):
    server.update()
    while not incoming_messages.empty():
        
    
    #let the CPU take a nap
    time.sleep(1.0/30.0)

    
    
if __name__ == '__main__':
    #init
    friends_list = []
    
    server = Server.Server()
    server.message(Server.OpCodes.state_changed, 'online')
    
    load_friends(friends_list)
    
    main_loop_thread = threading.Thread(target=main_loop, args[server]))
    main_loop_thread.deamon = True #won't keep the process up if main thread ends. not really necessary
    main_loop_thread.start()

    
    
    
    #init GUI
    
    
    
    
    #unload resources
    main_loop_thread.join()
    server.disconnect()
    for frnd in friends_list:
        frnd.close_chat_data_file()