__author__ = 'Аня'
import socket
from smtp import smtpClient
if __name__ == '__main__':
    print ('Введите команду: connect- установление соединения\r\nquit- разрыв соединения\r\nsend- отправка сообщения\r\nexit-выход из программы')
    sock=socket.socket()
    client=smtpClient(sock)
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
                    if(client.comConnect(server,25)==False):
                        print('Ошибка в команде connect!')
                    elif(client.helo('rambler.ru')==False):
                        print('Ошибка в команде helo')
                    else:
                        login=input('Введите логин')
                        password=input('Введите пароль')
                        if(client.setAuth(login,password)):
                            print("Аутентификация успешна")
                        else:
                            print('Ошибка при аутотенфикации')
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
                        if(client.sendMessage(mailFrom,rcptTo,ccString, bccString, subject, message)):
                            str="Сообщение отправлено: "
                            for i in client.set:
                                str=str+" "+i
                            print(str)
                        else:
                            print("Сообщение НЕ отправлено")
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
                    if(client.quit()):
                        print('Соединение разорвано!')
                    else:
                        print('Ошибка в команде quit')
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



