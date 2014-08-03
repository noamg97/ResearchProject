from Friend import Friend, StatusCodes
from Server import Server, OpCodes
import Shared
import Paths
import MessageParser
import UserInputParser
import MyData
import os
import threading
import time
import Queue

user_input = Queue.Queue()


def init_friends():
    #go through the data folders and for each file load a friend
    content = os.listdir(Paths.friends_data_path)
    for i in xrange(len(content)):
        cd = Paths.friends_data_path + Paths.slash + content[i]
        if not os.path.isdir(cd) and content[i].endswith(Paths.data_file_extension):
            f = Friend(content[i].split('.')[0])
            #append to the friends list
            Shared.friends_list.append(f)
    
        
def main():
    global should_exit
    global user_input
    global can_start_user_input
    
    #init
    Paths.check_all()
    Shared.my_data = MyData.MyData.load_user()
    Shared.server = Server()
    init_friends()
    print 'Friends List: { ' + ','.join([fr.data.username for fr in Shared.friends_list]) + ' }'
    parser = MessageParser.MessageParser()
    input_parser = UserInputParser.UserInputParser()
    
    can_start_user_input = True
    
    print '\nEntering main loop'
    print '\n------------\n'
    while not should_exit:
        #try:
        Shared.server.update()
        
        while not user_input.empty():
            should_exit = input_parser.parse(user_input.get())
            
        while not Shared.server.incoming_messages.empty():
            parser.parse(Shared.server.incoming_messages.get())
        
        for fd in Shared.friends_list:
            fd.update()
        
        #allow the CPU to take a nap
        time.sleep(1.0/30.0)
        #except:
            #exit nicely when an exception is raised. commented for easier debugging
        #    break
        
    Shared.server.disconnect()
    for frnd in Shared.friends_list:
        frnd.close()
    print 'Friends disconnected'
    
    
if __name__ == '__main__':
    should_exit = False
    can_start_user_input = False
    print '\n\n'

    main_loop_thread = threading.Thread(target=main) #maybe also pass friends_list
    main_loop_thread.start()

    while not can_start_user_input: pass
    
    #init GUI and main GUI loop
    while not should_exit:
        inp = raw_input()
        if inp.strip() == 'exit':
            should_exit = True
        user_input.put(inp)