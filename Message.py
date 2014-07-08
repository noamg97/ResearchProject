from datetime import datetime
class Message:
    def __init__(self, author, content, time=datetime.now()):
        self.author = author
        self.content = content
        self.time = time
    
    def to_data(self):
        return '{' + self.author + '}' + self.content + '{' + str(self.time) + '}' + '\n'
        
    def from_data(data_line):
        author = data_line[data_line.index('{')+1: data_line[data_line.index('{'):].index('}')]
        time = data_line[data_line.rindex('{')+1: data_line.rindex('}')]
        content = data_line[data_line.index('}')+1: data_line.rindex('{')]
        
        return Message(author, content, datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f'))
    
    def edit(self, new_content):
        self.content = new_content