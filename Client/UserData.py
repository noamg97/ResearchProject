import Message
import os
import Paths

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
        
        Paths.folder_safety(Paths.chat_data_path)
        
        self.load_data()

        
    @staticmethod
    def create_files(username):
        print 'creating files for ', username
        Paths.check_all()
        profile_data_file_path = Paths.friends_data_path + Paths.slash + username + Paths.data_file_extension
        chat_data_file_path = Paths.chat_data_path + Paths.slash + username + Paths.data_file_extension
                
        open(chat_data_file_path, 'a').close()
        open(profile_data_file_path, 'a').close()

        
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
            
    def change_profile_data(self, key, value):
        self.profile_data[key] = value
        self.save_data()
        
    def append_message_to_chat(self, message):
        self.chat_data.append(message)
        self.chat_data_file.write(message.to_data())
     
    def close_chat_data_file(self):
        self.chat_data_file.close()