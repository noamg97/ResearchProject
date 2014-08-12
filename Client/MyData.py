import Paths
import Shared
import os

class MyData:
    def __init__(self, username, password, state = 1):
        self.username = username
        self.password = password
        self.state = state
    
    @staticmethod
    def load_login_data():
        if not os.path.isfile(Paths.my_data_path):
            return False
            
        with open(Paths.my_data_path, 'r') as file:
            try:
                data = MyData()
                vars = {}
                for line in file.readlines():
                    key, value = [x.strip() for x in line.split(':')]
                    vars[key] = value
                
                
                Shared.my_data = MyData(vars['username'], vars['password'], vars['state'])
                return True
            except:
                print 'Corrupt Login Data File'
                
        return False