import Message
import os
from Paths import *

#chat data and profile data are stored in different files.
#chat data is a list of Massages (author, content, time)
#no field can contain a space character
class UserData:
    def __init__(self, id):
        self.id = id
    
        self.chat_data = []
        self.profile_data = {'username':'', 'fname':'', 'lname':'', 'picture':'', 'birthday':''}
        
        self.profile_data_file_path = friends_data_path + slash + self.id + data_file_extension
        self.chat_data_file_path = chat_data_path + slash + self.id + data_file_extension
        
        folder_safety(chat_data_path)
        
        self.load_data()

        
    def load_data(self):
        #load user profile data
        with open(self.profile_data_file_path, 'r') as file:
            try:
                data = file.readline().split(',')
                for part in data:
                    key, value = part.replace(' ', '').split(':')
                    self.profile_data[key] = value.strip()
            except:
                raise Exception('Corrupt Data File')
                
        #load chat data
        self.chat_data_file = open(self.chat_data_file_path, 'a+')
        self.chat_data_file.seek(0, os.SEEK_SET)
        for line in self.chat_data_file:
            self.chat_data.append(Message.Message.from_data(line))
        
    def save_data(self):
        data = ''
        for key, val in self.profile_data:
            data += key + ':' + val + ', '
            
        data = data[:len(data)-2] #remove the last ', '
        
        with open(self.profile_data_file_path, 'w') as file:
            file.write(data)
    
    def create_profile_data_file(self):
        open(self.profile_data_file_path, 'a').close()
        
    def change_profile_data(self, key, value):
        self.profile_data[key] = value
        self.save_data()
        
    def append_message_to_chat(self, message):
        self.chat_data.append(message)
        self.chat_data_file.write(message.to_data())
     
    def close_chat_data_file(self):
        self.chat_data_file.close()