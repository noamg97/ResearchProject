import Paths
import os

class MyData:
    def __init__(self, username):        
        self.data = { 'password':'', 'fname':'', 'lname':'' }
        self.username = username
        #with open(Paths.my_data_path, 'r') as file:
        #    try:
        #        data = file.readline().split(',')
        #        for part in data:
        #            key, value = part.replace(' ', '').split(':')
        #            self.profile_data[key] = value.strip()
        #    except:
        #        raise Exception('Corrupt Data File')

    @staticmethod
    def load_user():
        return MyData(raw_input('Please select a username: '))