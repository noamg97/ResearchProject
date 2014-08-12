from datetime import datetime
import Shared

class Message:
    def __init__(self, author, content, time=datetime.now()):
        self.author = author
        self.content = content
        self.time = time
    
    def to_data(self):
        return '{' + self.author + '}' + self.content + '{' + str(self.time) + '}' + '\n'
        
    @staticmethod
    def from_data(data_line):
        author = data_line[data_line.index('{')+1: data_line[data_line.index('{'):].index('}')]
        time = data_line[data_line.rindex('{')+1: data_line.rindex('}')]
        content = data_line[data_line.index('}')+1: data_line.rindex('{')]
        
        return Message(author, content, datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f'))
    
    def to_readable(self):
        return '[' + str(self.time) + '] ' + self.author + ': ' + self.content
    
    def edit(self, new_content):
        self.content = new_content