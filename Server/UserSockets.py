import socket

class UserSockets():
    def __init__(self, main_socket):
        self.main_socket = main_socket
        self.sleeping_sockets = []

    def send(self, msg):
        self.main_socket.send(msg + ';')
        
    def all(self):
        return [self.main_socket] + self.sleeping_sockets
        
    def append(self, sleeping_sock):
        self.sleeping_sockets.append(sleeping_sock)
     #TODO: add try & except v^
    def remove(self, sleeping_sock):
        self.sleeping_sockets.remove(sleeping_sock)
        
    def use_sleeping(self):
        sock = self.sleeping_sockets[0]
        del self.sleeping_sockets[0]
        
        return sock.getpeername()
        
    def close(self):
        self.main_socket.close()
        for s in self.sleeping_sockets:
            try: s.close()
            except: pass