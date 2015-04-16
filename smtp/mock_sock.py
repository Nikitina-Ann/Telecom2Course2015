__author__ = 'Аня'
import socket
import random
class MockSocketTrue(socket.socket):
    message=''
    auth=False
    data=False
    var=1
    bool=False
    hasError=False
    def getBool(self):
        if(self.hasError==False):
            self.bool=True
        else:
            self.bool=random.choice([True,False])
    def connect(self, ser):
        self.getBool()
        if(self.bool==False):
            self.message=b'500'
        else:
            self.message=b'220'
    def send(self, string):
        string=string[:4]
        self.getBool()
        if(self.bool==False):
            self.message=b'500'
        elif(string==b'HELO' or string==b'MAIL' or string==b'RCPT' or self.data==True):
            self.message=b'250'
            self.data=False
        elif(string==b'AUTH'):
            self.auth=True
            self.var=1
            self.message=b'334'
        elif(string==b'DATA'):
             self.message=b'354'
             self.data=True
        elif(string==b'QUIT'):
             self.message=b'221'
        elif(self.auth==True):
            if(self.var==1):
                self.message=b'334'
            if(self.var==2):
                self.message=b'235'
                self.auth=False
            self.var=self.var+1
    def recv(self, bytes):
        return self.message

class MockSocketFalse(socket.socket):
    message=''
    def connect(self, ser):
        self.message=b'500'
    def send(self, string):
        self.message=b'500'
    def recv(self, bytes):
        return self.message