import UserData

class Friend:
    def __init__(self, id):
        self.data = UserData(id)
        
    def connect(self):
        
        
    def get_chat(self):
        return self.data.chat_data
        
    def close_chat_data_file(self):
        self.data.close_chat_data_file()