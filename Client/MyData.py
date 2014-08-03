import Paths
from Server import OpCodes
import os

class MyData:
    def __init__(self, username, password, is_new_user, status = 1):
        self.username = username
        self.password = password
        self.is_new_user = is_new_user
        self.status = status
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
        choice = raw_input('Type "c" to create a new user, or anything else to proceed to login').strip().lower()
        u = raw_input('Please type in your username: ')
        p = raw_input('Please type in your password: ')
        
        return MyData(u, p, choice == 'c')