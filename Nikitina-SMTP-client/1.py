__author__ = 'Аня'
import socket
import base64
def sendCommandToServer(com):
    sock.send(com)
    return sock.recv(1024)
def encrBase64(string):
     string=base64.b64encode(bytes(string,encoding = 'utf-8'))+b'\r\n'
     return string
def comConnect(string):
    connect=True
    sock.connect((string, 25))
    answer = sock.recv(1024)
    if(answer[0:3]!=b'220'):
        print('Error  in connect')
        connect=False
    return connect
def helo(string):
    answer=sendCommandToServer(b'HELO '+ bytes(string,encoding = 'utf-8')+b'\r\n')
    if(answer[0:3]!=b'250'):
       print('Error  in helo')
def auth(login,password):
    answer=sendCommandToServer(b'AUTH LOGIN\r\n')
    if(answer[0:3]==b'334'):
        login=encrBase64(login)
        answer=sendCommandToServer(login)
        if(answer[0:3]!=b'334'):
            print('Error  in login')
        else:
            password=encrBase64(password)
            answer=sendCommandToServer(password)
            if(answer[0:3]!=b'235'):
                 print('Error  in password')
    else:
        print('Error  in authenticating')
def sendFromTo(com,string):
    if(com=='mailFrom'):
        bit_com=b'MAIL FROM: '
    elif(com=='rcptTo'):
        bit_com=b'RCPT TO: '
    string=bit_com+bytes(string,encoding = 'utf-8')+b'\r\n'
    answer=sendCommandToServer(string)
    if(answer[0:3]!=b'250'):
        print('Error  in adrress '+ com)
def bccCcRcpt(string):
    string=string.split(',')
    for i in string:
        sendFromTo('rcptTo',i)
def sendData(mailFrom, rcptTo, ccString, bccString, subject, message):
    data=b'From: '+bytes(mailFrom,encoding = 'utf-8')+b'\r\n'
    data=data+b'To: '+bytes(rcptTo,encoding = 'utf-8')+b'\r\n'
    data=data+b'Reply-To: '+bytes(mailFrom,encoding = 'utf-8')+b'\r\n'
    data=data+b'Subject: '+bytes(subject,encoding = 'utf-8')+b'\r\n'
    data=data+b'nContent-Transfer-Encoding: base64\r\n'
    data=data+b'Content-Type: text/plain; charset=ISO-8859-1\r\n'
    data=data+b'BCC: '+bytes(bccString,encoding = 'utf-8')+b'\r\n'
    data=data+b'CC: '+bytes(ccString,encoding = 'utf-8')+b'\r\n'
    data=data+bytes(message,encoding = 'utf-8')+b'\r\n.\r\n'
    return data
def quit():
    answer=sendCommandToServer(b'QUIT\r\n')
    if(answer[0:3]==b'221'):
        connect=False
        sock.close()
    else:
        print('Error in quit')
        connect=True
    return connect


connect=False
print ('Введите команду: connect- установление соединения\r\nquit- разрыв соединения\r\nsend- отправка сообщения\r\nexit-выход из программы')
command=input()
while(command!='exit'):
    if(command=='connect'):
        if(connect==False):
            sock = socket.socket()
            connect=comConnect('smtp.rambler.ru')
            helo('rambler.ru')
        else:
            print('Ошибка. Соединение уже установлено!')
    elif(command=='send'):
        if(connect==True):
            print ('Введите логин')
            login=input()
            print ('Введите пароль')
            password=input()
            auth(login,password)
            print ('Введите адрес отправителя')
            mailFromAdrr=input()
            sendFromTo('mailFrom',mailFromAdrr)
            print ('Введите адрес получателя')
            rcptToAdrr=input()
            sendFromTo('rcptTo', rcptToAdrr)

            print ('Введите bcc адреса через запятую (,)')
            bccString=input()
            print ('Введите cc адреса через запятую (,)')
            ccString=input()
            print ('Введите тему сообщения')
            subject=input()
            print ('Введите сообщение')
            message=input()

            bccCcRcpt(bccString)
            bccCcRcpt(ccString)
            answer=sendCommandToServer(b'DATA\r\n')
            if(answer[0:3]==b'354'):
                data=sendData(mailFromAdrr,rcptToAdrr,ccString,bccString,subject,message)
                print(data)
                answer=sendCommandToServer(data)
                if(answer[0:3]!=b'250'):
                    print('Error  in data')
            else:
                print('Error  in data')
        else:
            print('Ошибка. Для начала надо установить соединение. Команда CONNECT!')
    elif(command=='quit'):
        if(connect==True):
              connect= quit()
        else:
               print('Ошибка. Соединение не установлено.')
    else:
        print('Ошибка. Такой команды нет!')
    command=input()

print('Выход их программы')



