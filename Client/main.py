from Friend import Friend, stateCodes
from Server import Server, OpCodes
import Shared
import Paths
import MessageParser
import UserInputParser
import MyData

import MainWindow
import LoginWindow

import os
import threading
import time
import Queue



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
    global init_finished
    
    #init
    Paths.check_all()
    Shared.server.init_sleeping_sockets()
    init_friends()
    print 'Friends List: { ' + ','.join([fr.data.username for fr in Shared.friends_list]) + ' }'
    parser = MessageParser.MessageParser()
    
    init_finished = True
    
    print '\nEntering main loop'
    print '\n------------\n'
    while not should_exit:
        #try:
        Shared.server.update()
        
        while not Shared.server.incoming_messages.empty():
            parser.parse(Shared.server.incoming_messages.get())
        
        for fd in Shared.friends_list:
            fd.update()
        
        #allow the CPU to take a nap
        time.sleep(1.0/30.0)
        #except:
            #exit nicely when an exception is raised.
        #    break
        
    print '\nExited main loop'
    Shared.server.disconnect()
    for frnd in Shared.friends_list:
        frnd.close()
    print 'Friends disconnected'
    
    
if __name__ == '__main__':
    should_exit = False
    init_finished = False
    print '\n\n'

    #Shared.server = Server()
    
    #l_window = LoginWindow.LoginWindow()
    #l_window.main()
    #del l_window
    
    #main_loop_thread = threading.Thread(target=main)
    #main_loop_thread.start()
    
    #while not init_finished: pass
    
    
    #init GUI and main GUI loop
    m_window = MainWindow.MainWindow()
    m_window.main()
    
    should_exit = True
    #main_loop_thread.join()
    
    print 'exited'
    #raw_input()