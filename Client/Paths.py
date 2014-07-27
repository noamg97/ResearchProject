import sys, os

app_data_path = 'KoalaChat' #TODO: think of an actual name
slash = '\\'



if sys.platform == 'win32':
    app_data_path = os.getenv('APPDATA') + '\\' + app_data_path
    
if sys.platform == 'linux2':
    app_data_path = os.path.expanduser("~") + '/' + app_data_path
    slash = '/'
    
if sys.platform == 'darwin':
    app_data_path = '~/Library/Application Support/' + app_data_path #TODO: check if this works
    slash = '/'

    
friends_data_path = app_data_path + slash + 'Friends'
chat_data_path = app_data_path + slash + 'Chat'

data_file_extension = '.dat' #TODO: .dat files..?

my_data_path = app_data_path + slash + 'Me' + data_file_extension

def check_all():
    folder_safety(friends_data_path)
    folder_safety(chat_data_path)
    
def folder_safety(folder):
    if not os.path.exists(folder):
        print 'creating folder ' + folder
        os.makedirs(folder)
