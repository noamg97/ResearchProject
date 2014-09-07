import Message
import os
import Paths
import Shared
from datetime import datetime

#chat data and profile data are stored in different files.
#chat data is a list of Massages (author, content, time)
#no field can contain a space character
class UserData:
    def __init__(self, username):
        self.username = username
    
        self.chat_data = []
        self.profile_data = { 'fname':'', 'lname':'', 'picture':'', 'birthday':''}
        
        self.profile_data_file_path = Paths.friends_data_path + Paths.slash + self.username + Paths.data_file_extension
        self.chat_data_file_path = Paths.chat_data_path + Paths.slash + self.username + Paths.data_file_extension
        
        Paths.check_all()
        Paths.file_safety(self.profile_data_file_path)
        Paths.file_safety(self.chat_data_file_path)
        
        self.load_data()

        
    def load_data(self):
        #load user profile data
        with open(self.profile_data_file_path, 'r') as file:
            try:
                data = file.readline().split(',')
                fields = [m for m in data if m != '']
                for part in fields:
                    key, value = part.replace(' ', '').split(':')
                    self.profile_data[key] = value.strip()
            except:
                raise Exception('Corrupt Profile Data File; Username:' + self.username)
                
                
        #load chat data
        self.chat_data_file = open(self.chat_data_file_path, 'a+')
        self.chat_data_file.seek(0, os.SEEK_SET)
        
        #author,time,msg_length,msg
        #try:
        all = self.chat_data_file.read()
        num = 0
        while num < len(all):
            msg_data = []
            for i in xrange(3):
                data = ''
                c = all[num]
                while c != ',':
                    data += c
                    num+=1
                    c = all[num]
                num+=1
                msg_data.append(data)
            
            msg = all[num:num+int(msg_data[2])]
            num += int(msg_data[2])
            self.chat_data.append(Message.Message(msg_data[0], msg, datetime.strptime(msg_data[1], '%Y-%m-%d %H:%M:%S.%f')))
        self.chat_data_file.seek(0, 2)
        #except:
        #    raise Exception('Corrupt Chat Data File; Username:' + self.username)
        
    def save_data(self):
        data = ''
        for key, val in self.profile_data:
            data += key + ':' + val + ', '
            
        data = data[:len(data)-2] #remove the last ', '
        
        with open(self.profile_data_file_path, 'w') as file:
            file.write(data)
            
    def change_profile_data(self, key, value):
        self.profile_data[key] = value
        self.save_data()
        
    def append_message_to_chat(self, message):
        if not any(self.chat_data):
            Shared.main_window.calls.put((Shared.main_window.append_active_chat, self.username))
            
        self.chat_data.append(message)
        self.chat_data_file.seek(0, 2)
        self.chat_data_file.write(message.to_data())
        
    def close_chat_data_file(self):
        self.chat_data_file.close()