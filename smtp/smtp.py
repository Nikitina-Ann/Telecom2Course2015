__author__ = 'Аня'
import base64
class smtpClient:
    def __init__ (self,sock):
        self.connect = False
        self.auth=False
        self.set=[]
        self.sock = sock
    def sendCommandToServer(self,com):
        self.sock.send(com)
        return self.sock.recv(1024)
    def encrBase64(self,string):
        string=base64.b64encode(bytes(string,encoding = 'utf-8'))+b'\r\n'
        return string
    def comConnect(self,string,port):
        self.sock.connect((string, port))
        answer = self.sock.recv(1024)
        self.connect=True
        if(answer[0:3]!=b'220'):
            self.connect=False
            return False
        return True

    def helo(self,string):
        answer=self.sendCommandToServer(b'HELO '+ bytes(string,encoding = 'utf-8')+b'\r\n')
        if(answer[0:3]!=b'250'):
            return False
        return True
    def setAuth(self,login,password):
        answer=self.sendCommandToServer(b'AUTH LOGIN\r\n')
        if(answer[0:3]!=b'334'):
            self.connect=False
            return False
        else:
            login=self.encrBase64(login)
            answer=self.sendCommandToServer(login)
            if(answer[0:3]!=b'334'):
                self.connect=False
                return False
            else:
                password=self.encrBase64(password)
                answer=self.sendCommandToServer(password)
                if(answer[0:3]!=b'235'):
                    self.connect=False
                    return False
            self.auth=True
            return True
    def sendFromTo(self,com,string):
        if(com=='mailFrom'):
            bit_com=b'MAIL FROM: '
        elif(com=='rcptTo'):
            bit_com=b'RCPT TO: '
        stringNew=bit_com+bytes(string,encoding = 'utf-8')+b'\r\n'
        answer=self.sendCommandToServer(stringNew)
        if(answer[0:3]!=b'250'):
            #print('Ошибка в адресе '+ com+' '+string)
            return False
        return True
    def bccCcRcpt(self,string):
        if(len(string)!=0):
            string=string.split(',')
        return string

    def sendUsers(self,rcptTo):
        rcptTo=self.bccCcRcpt(rcptTo)
        for i in rcptTo:
            if(self.sendFromTo('rcptTo',i)==True and (i in self.set)==False):
                self.set.append(i)
    def data(self,mailFrom, rcptTo, ccString, bccString, subject, message):
        data=b'From: '+bytes(mailFrom,encoding = 'utf-8')+b'\r\n'
        rcptTo=self.bccCcRcpt(rcptTo)
        for i in rcptTo:
            data=data+b'To: '+bytes(i,encoding = 'utf-8')+b'\r\n'
        data=data+b'Reply-To: '+bytes(mailFrom,encoding = 'utf-8')+b'\r\n'
        data=data+b'Subject: '+bytes(subject,encoding = 'utf-8')+b'\r\n'
        data=data+b'nContent-Transfer-Encoding: base64\r\n'
        data=data+b'Content-Type: text/plain; charset=ISO-8859-1\r\n'
        if(len(bccString)!=0):
           data=data+b'BCC: '+bytes(bccString,encoding = 'utf-8')+b'\r\n'
        if(len(ccString)!=0):
            data=data+b'CC: '+bytes(ccString,encoding = 'utf-8')+b'\r\n'
        data=data+bytes(message,encoding = 'utf-8')+b'\r\n.\r\n'
        return data
    def sendData(self,data):
        answer=self.sendCommandToServer(b'DATA\r\n')
        if(answer[0:3]==b'354'):
            answer=self.sendCommandToServer(data)
            if(answer[0:3]==b'250'):
                return True
        return False
    def sendMessage(self,mailFrom,rcptTo,ccString, bccString, subject, message):
        self.set=[]
        if(self.sendFromTo('mailFrom',mailFrom)==False):
            return False
        self.sendUsers(rcptTo)
        if(len(self.set)==0):
            return False
        self.sendUsers(bccString)
        self.sendUsers(ccString)
        data=self.data(mailFrom,rcptTo,ccString,bccString,subject,message)
        send=self.sendData(data)
        return send
    def quit(self):
        answer=self.sendCommandToServer(b'QUIT\r\n')
        if(answer[0:3]==b'221'):
            self.sock.close()
            self.auth=False
            self.connect=False
            return True
        else:
            return False

    def rset(self):
        self.auth=False
        self.connect=False


