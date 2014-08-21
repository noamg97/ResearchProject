from datetime import datetime
import Shared

class Message:
    def __init__(self, author, content, time=datetime.now()):
        self.author = author
        self.content = content
        self.time = time
    
    #author,time,msg_length,msg
    def to_data(self):
        msg = str(self.content)
        return str(self.author) + ',' + str(self.time) + ',' + str(len(msg)) + ',' + msg
    
    @staticmethod
    def from_data(data):
        num = 0
        while num < len(data):
            msg_data = []
            for i in xrange(3):
                field = ''
                c = data[num]
                while c != ',':
                    field += c
                    num+=1
                    c = data[num]
                num+=1
                msg_data.append(field)
            
            msg = data[num:num+int(msg_data[2])]
            num += int(msg_data[2])
        return Message(msg_data[0], msg, datetime.strptime(msg_data[1], '%Y-%m-%d %H:%M:%S.%f'))
    
    def to_console(self):
        return '[' + str(self.time) + '] ' + str(self.author) + ': '+ str(self.content)
    
    def edit(self, new_content):
        self.content = new_content