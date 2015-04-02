__author__ = 'Аня'
import socket
import base64
class MyError(Exception):
    def __init__ (self,text):
       self.txt =text
class smtpClient:
    def __init__ (self):
        self.connect = False
        self.auth=False
        self.set=[]
        self.sock = socket.socket()
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
            print('Ошибка в команде connect!')
            return False
        return True

    def helo(self,string):
        answer=self.sendCommandToServer(b'HELO '+ bytes(string,encoding = 'utf-8')+b'\r\n')
        if(answer[0:3]!=b'250'):
            print('Ошибка в команде helo')
            return False
        return True
    def setAuth(self,login,password):
        answer=self.sendCommandToServer(b'AUTH LOGIN\r\n')
        if(answer[0:3]!=b'334'):
            self.connect=False
            print('Ошибка при аутотенфикации')
            return False
        else:
            login=self.encrBase64(login)
            answer=self.sendCommandToServer(login)
            if(answer[0:3]!=b'334'):
                self.connect=False
                print('Ошибка в команде login')
                return False
            else:
                password=self.encrBase64(password)
                answer=self.sendCommandToServer(password)
                if(answer[0:3]!=b'235'):
                    self.connect=False
                    print('Ошибка в команде password')
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
            print('Ошибка в адресе '+ com+' '+string)
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
        if(send==True):
            str="Сообщение отправлено: "
            for i in self.set:
                str=str+" "+i
            print(str)
        else:
            print("Сообщение НЕ отправлено")
        return send
    def quit(self):
        answer=self.sendCommandToServer(b'QUIT\r\n')
        if(answer[0:3]==b'221'):
            self.sock.close()
            self.auth=False
            self.connect=False
            print('Соединение разорвано!')
            return True
        else:
            print('Ошибка в команде quit')
            return False

    def rset(self):
        self.auth=False
        self.connect=False


if __name__ == '__main__':
    print ('Введите команду: connect- установление соединения\r\nquit- разрыв соединения\r\nsend- отправка сообщения\r\nexit-выход из программы')
    client=smtpClient()
    while(1):
        try:
            command=input('Введите команду:')
            if(command=='connect'):
                if(client.connect==True):
                    client.rset()
                    print("Предыдущее соединение разорвано")
                server=input('Введите название сервера: ')
                client.sock = socket.socket()
                    #smtp.rambler.ru
                try:
                    if(client.comConnect(server,25) and client.helo('rambler.ru')):
                        login=input('Введите логин')
                        password=input('Введите пароль')
                        if(client.setAuth(login,password)):
                            print("Аутотенфикация успешна")
                except socket.gaierror:
                    print("Ошибка При вызове функции connect!\r\n")
                except EOFError:
                    print("Ошибка ввода!\r\n")
            elif(command=='send'):
                if(client.auth==True and client.connect==True):
                    try:
                        mailFrom=input('Введите адрес отправителя')
                        rcptTo=input('Введите адрес получателЕй через запятую (,)')
                        bccString=input('Введите bcc адреса через запятую (,)')
                        ccString=input('Введите cc адреса через запятую (,)')
                        subject=input('Введите тему сообщения')
                        message=input('Введите сообщение')
                        client.sendMessage(mailFrom,rcptTo,ccString, bccString, subject, message)
                    except EOFError:
                        print("Ошибка ввода!\r\n")
                        continue
                    except  UnicodeEncodeError:
                        print ('Ошибка при кодировании в unicode!')
                        continue
                else:
                    print('Ошибка. Для начала надо установить соединение. Команда CONNECT!')
            elif(command=='quit'):
                if(client.connect==True):
                    client.quit()
                else:
                    print('Ошибка. Соединение не установлено.')
            elif(command=='exit'):
                    print('Выход их программы')
                    break
            else:
                print('Ошибка. Такой команды нет!')
        except EOFError:
            print("Ошибка ввода!\r\n")
            client.connect=False
            client.auth=False
            break



