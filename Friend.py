import UserData

class Friend:
    def __init__(self, username):
        self.data = UserData(username)
        
    def get_chat(self):
        return self.data.chat_data
        
    def close_chat_data_file(self):
        self.data.close_chat_data_file()