from Friend import Friend
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



def main():
    global should_exit
    global server_init_finished, gui_init_finished
    
    #init
    Shared.server.init_sleeping_sockets()
    print 'Friends List: { ' + ','.join([fr.data.username for fr in Shared.friends_list]) + ' }'
    
    server_init_finished = True
    while not gui_init_finished: pass
    
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
    server_init_finished = False
    gui_init_finished = False
    print '\n\n'

    Shared.server = Server()
    
    l_window = LoginWindow.LoginWindow()
    _continue = l_window.main()
    l_window.destroy()
    
    if _continue:
        main_loop_thread = threading.Thread(target=main)
        main_loop_thread.start()
        
        while not server_init_finished: pass
        
        
        #init GUI and main GUI loop
        Shared.main_window = MainWindow.MainWindow()
        gui_init_finished = True
        Shared.main_window.main()
        
        should_exit = True
        main_loop_thread.join()
        
    print 'exited'