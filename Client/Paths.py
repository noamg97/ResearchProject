import sys, os

app_data_path = 'Whoosh' #TODO: think of an actual name ::: ResearchProject / Whoosh / Sqwush
slash = '\\'



if sys.platform == 'win32':
    app_data_path = os.getenv('APPDATA') + '\\' + app_data_path
    
if sys.platform == 'linux2':
    app_data_path = os.path.expanduser("~") + '/' + app_data_path
    slash = '/'
    
if sys.platform == 'darwin':
    app_data_path = os.path.expanduser("~") + '/Library/Application Support/' + app_data_path #TODO: check if this works
    slash = '/'

data_file_extension = '.dat' #TODO: .dat?
friends_data_path=''
chat_data_path=''
my_data_path=''

#called from Server.send_login_request() after server accepts user's login
def init(username):
    global app_data_path, slash, my_data_path, friends_data_path, chat_data_path, my_data_path, data_file_extension
    
    app_data_path += slash + str(username)
    friends_data_path = app_data_path + slash + 'Friends'
    chat_data_path = app_data_path + slash + 'Chat'
    
    my_data_path = app_data_path + slash + 'Me' + data_file_extension
    
    check_all()


def check_all():
    folder_safety(friends_data_path)
    folder_safety(chat_data_path)
    #open(my_data_path, 'a').close()

    
def folder_safety(folder):
    if not os.path.exists(folder):
        print 'creating folder ' + folder
        os.makedirs(folder)


def file_safety(path):
    open(path, 'a').close()