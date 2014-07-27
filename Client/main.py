from Friend import Friend, StatusCodes
from Server import Server, OpCodes
import Shared
import Paths
import MessageParser
import UserInputParser
import os
import threading
import time
import Queue

user_input = Queue.Queue()

def init_my_data():
    with open(Paths.my_data_path, 'r') as file:
        Shared.my_id = file.read().strip()
        print 'My id: ' + Shared.my_id

def init_friends():
    #go through the data folders and for each file load a friend
    Paths.folder_safety(Paths.friends_data_path)
    content = os.listdir(Paths.friends_data_path)
    for i in xrange(len(content)):
        cd = Paths.friends_data_path + Paths.slash + content[i]
        if not os.path.isdir(cd) and content[i].endswith(Paths.data_file_extension):
            f = Friend(content[i].split('.')[0])
            #append to the friends list
            Shared.friends_list.append(f)
            #ask the server for his current status
            Shared.server.message(OpCodes.ask_for_status, f.data.id)
    
        
def main():
    global should_exit
    global user_input
    
    #init
    init_my_data()
    Shared.server = Server(Shared.my_id)
    Shared.server.message(OpCodes.my_state_changed, StatusCodes.online)
    init_friends()
    print 'Friends List: { ' + ','.join([fr.data.profile_data['username'] for fr in Shared.friends_list]) + ' }'
    parser = MessageParser.MessageParser()
    input_parser = UserInputParser.UserInputParser()
    
    print '\nEntering main loop'
    print '\n------------\n'
    while not should_exit:
        Shared.server.update()
        
        while not user_input.empty():
            input_parser.parse(user_input.get())
            
        while not Shared.server.incoming_messages.empty():
            parser.parse(Shared.server.incoming_messages.get())
        
        for fd in Shared.friends_list:
            fd.update()
        
        #allow the CPU to take a nap
        time.sleep(1.0/30.0)

        
    Shared.server.disconnect()
    for frnd in Shared.friends_list:
        frnd.close()
    print 'Friends disconnected'
    
    
if __name__ == '__main__':
    should_exit = False
    print '\n\n'

    main_loop_thread = threading.Thread(target=main) #maybe also pass friends_list
    main_loop_thread.start()

    
    #init GUI and main GUI loop
    try:
        while True:
            user_input.put(raw_input())
    except KeyboardInterrupt:
        pass
    
    print 'Exiting...'
    
    #unload resources
    should_exit = True
    main_loop_thread.join()