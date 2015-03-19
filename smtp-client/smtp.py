__author__ = 'Аня'
import socket
import base64
class MyError(Exception):
    def __init__ (self,text):
       self.txt =text
class smtpClient:
    def __init__ (self):
        self.connect = False
        self.sock = socket.socket()
    def sendCommandToServer(self,com):
        self.sock.send(com)
        return self.sock.recv(1024)
    def encrBase64(self,string):
        string=base64.b64encode(bytes(string,encoding = 'utf-8'))+b'\r\n'
        return string
    def comConnect(self,string):
        self.sock.connect((string, 25))
        answer = self.sock.recv(1024)
        if(answer[0:3]!=b'220'):
            print('Ошибка в функции connect!')
        else:
            self.connect=True

    def helo(self,string):
        answer=self.sendCommandToServer(b'HELO '+ bytes(string,encoding = 'utf-8')+b'\r\n')
        if(answer[0:3]!=b'250'):
            print('Error  in helo')
            self.connect=False
    def auth(self,login,password):
        answer=self.sendCommandToServer(b'AUTH LOGIN\r\n')
        if(answer[0:3]!=b'334'):
            self.connect=False
            print('Ошибка при аутотенфикации')
        else:
            login=self.encrBase64(login)
            answer=self.sendCommandToServer(login)
            if(answer[0:3]!=b'334'):
                self.connect=False
                print('Ошибка в команде login')
            else:
                password=self.encrBase64(password)
                answer=self.sendCommandToServer(password)
                if(answer[0:3]!=b'235'):
                    self.connect=False
                    print('Ошибка в команде password')
    def sendFromTo(self,com,string):
        if(com=='mailFrom'):
            bit_com=b'MAIL FROM: '
        elif(com=='rcptTo'):
            bit_com=b'RCPT TO: '
        string=bit_com+bytes(string,encoding = 'utf-8')+b'\r\n'
        answer=self.sendCommandToServer(string)
        if(answer[0:3]!=b'250'):
            print('Ошибка в адресе '+ com)
            self.connect=False
    def bccCcRcpt(self,string):
        if(len(string)!=0):
            string=string.split(',')
            for i in string:
                self.sendFromTo('rcptTo',i)
    def sendData(self,mailFrom, rcptTo, ccString, bccString, subject, message):
        data=b'From: '+bytes(mailFrom,encoding = 'utf-8')+b'\r\n'
        data=data+b'To: '+bytes(rcptTo,encoding = 'utf-8')+b'\r\n'
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
    def sendMessage(self,data):
        answer=self.sendCommandToServer(b'DATA\r\n')
        if(answer[0:3]==b'354'):
            answer=self.sendCommandToServer(data)
            if(answer[0:3]!=b'250'):
                print('Ошибка в команде data')
                self.connect=False
            else:
                print('Сообщение отправлено')
        else:
            print('Ошибка в команде data')
            self.connect=False

    def quit(self):
        answer=self.sendCommandToServer(b'QUIT\r\n')
        if(answer[0:3]==b'221'):
            self.connect=False
            self.sock.close()
        else:
            print('Ошибка в команде quit')


if __name__ == '__main__':
    print ('Введите команду: connect- установление соединения\r\nquit- разрыв соединения\r\nsend- отправка сообщения\r\nexit-выход из программы')
    client=smtpClient()
    while(1):
        try:
            command=input('Введите команду:')
            if(command=='connect'):
                if(client.connect==False):
                    server=input('Введите название сервера: ')
                    client.sock = socket.socket()
                        #smtp.rambler.ru
                    try:
                        string=client.comConnect(server)
                        client.helo('rambler.ru')
                        continue
                    except socket.gaierror:
                        print("Ошибка При вызове функции connect!\r\n")
                else:
                    print('Соединение уже установлено!')
            elif(command=='send'):
                if(client.connect==True):
                    try:
                        login=input('Введите логин')
                        password=input('Введите пароль')
                        client.auth(login,password)
                        if(client.connect==False):
                            continue
                        mailFromAdrr=input('Введите адрес отправителя')
                        client.sendFromTo('mailFrom',mailFromAdrr)
                        if(client.connect==False):
                            continue
                        rcptToAdrr=input('Введите адрес получателя')
                        client.sendFromTo('rcptTo', rcptToAdrr)
                        if(client.connect==False):
                            continue

                        bccString=input('Введите bcc адреса через запятую (,)')
                        ccString=input('Введите cc адреса через запятую (,)')
                        subject=input('Введите тему сообщения')
                        message=input('Введите сообщение')

                        client.bccCcRcpt(bccString)
                        if(client.connect==False):
                            continue
                        client.bccCcRcpt(ccString)
                        if(client.connect==False):
                            continue
                        data=client.sendData(mailFromAdrr,rcptToAdrr,ccString,bccString,subject,message)
                        client.sendMessage(data)
                    except EOFError:
                        print("Ошибка ввода!\r\n")
                        client.connect=False
                        continue
                    except  UnicodeEncodeError:
                        print ('Ошибка при кодировании в unicode!')
                        client.connect=False
                        continue
                else:
                    print('Ошибка. Для начала надо установить соединение. Команда CONNECT!')
            elif(command=='quit'):
                if(client.connect==True):
                    client.quit()
                    if(client.connect==False):
                        print('Соединение разорвано!')
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
            break



