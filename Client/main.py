from Friend import Friend, stateCodes
from Server import Server
import OpCodes
import Shared
import Paths
import UserInputParser
import MyData

import MainWindow
import LoginWindow

import os
import threading
import time
import Queue
import traceback
import sys



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
    Shared.server.init_sleeping_sockets()
    init_friends()
    print 'Friends List: { ' + ','.join([fr.data.username for fr in Shared.friends_list]) + ' }'
    
    init_finished = True
    
    print '\nEntering main loop'
    print '\n------------\n'
    while not should_exit:
        try:
            Shared.server.update()
                        
            for fd in Shared.friends_list:
                fd.update()
        
            #allow the CPU to take a nap
            time.sleep(1.0/30.0)
        except Exception as ex:
            #exit nicely when an exception is raised.
            print '\n', traceback.format_exc()
            #for frame in traceback.extract_tb(sys.exc_info()[2]):
            #    fname,lineno,fn,text = frame
            #    print "--->%s in %s on line %d\nException Arguments: %s" % (type(ex).__name__, fname, lineno, ex.args)
            break
        
    print '\nExited main loop'
    
    Shared.server.disconnect()
    for frnd in Shared.friends_list:
        frnd.close()
    print 'Friends disconnected'
    while not Shared.main_window: pass
    Shared.main_window.destroy()
    
    
if __name__ == '__main__':
    should_exit = False
    init_finished = False
    print '\n\n'

    Shared.server = Server()
    
    l_window = LoginWindow.LoginWindow()
    _continue = l_window.main()
    l_window.destroy()
    
    if _continue:
        main_loop_thread = threading.Thread(target=main)
        main_loop_thread.start()
        
        while not init_finished: pass
        
        
        #init GUI and main GUI loop
        Shared.main_window = MainWindow.MainWindow()
        Shared.main_window.main()
        
        should_exit = True
        main_loop_thread.join()
        
    print 'exited'